import discord
from discord.ext import commands

#import logging
from dotenv import load_dotenv
import os
import asyncio

#custom files
from DataClass.GuildSettings import GuildSettings

from PermissionManager.PermissionManager import PermissionManager
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from APIRequester.APIManager import APIManager

from Discord.View.ErrorMessageView import ErrorMessageView
from Discord.View.MinorFactionView import MinorFactionView
from Discord.View.SystemView import SystemView
from Discord.View.SystemRecap.SystemsRecapViews import SystemsRecapViews
from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
from Discord.View.SystemRecap.SystemRecapLegendView import SystemsRecapLegendView
from Discord.View.SystemRecap.Warning.ExpansionWarningSystemsRecapView import ExpansionWarningSystemsRecapView
from Discord.View.GuildSettings.DefaultGuildSettingsView import DefaultGuildSettingsView
from Discord.View.MissionsRecap.MissionsRecapViews import MissionsRecapViews

from Discord.View.SystemEventLog.MinorFactionJoinSystemEventLogView import MinorFactionJoinSystemEventLogView
from Discord.View.SystemEventLog.MinorFactionLeaveSystemEventLogView import MinorFactionLeaveSystemEventLogView

from Discord.View.APIMonitorView import APIMonitorView

from BotConfig.BotConfig import BotConfig
BotConfig.load()


#Discord app token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

guildIDs_raw = os.getenv("DISCORD_GUILDS")
guildIDs = [int(guildID) for guildID in guildIDs_raw.split(",") if guildID]
print(guildIDs)

#Permission manager
PermissionManager.set_super_admin_id(int(os.getenv("SUPER_ADMIN")))

#Intents for discord
intents = discord.Intents.default()
intents.message_content = True

#create bot
bot = discord.Bot(intents=intents)


#update file check
for guild_id in guildIDs:
    DataStorageManager.create_missing_data_files(guild_id)


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    print(f"Guilds : {[g.name for g in bot.guilds]}")


####################################################################
####################################################################
def isBotMessage(message) -> bool:
    return message.author == bot.user

####################################################################
#################################################################### slash command

@bot.slash_command(name="forceupdatebgsdata", description="force the update of minor faction systems bgs data", guild_ids=guildIDs)
async def forceupdatebgsdata(ctx: discord.ApplicationContext):
    await ctx.defer()
    system_events = await asyncio.to_thread(DataManager.updateStoredSystemsBGSData, ctx.guild_id)
    await ctx.edit(content="Systems BGS Data Updated Successfully!")
    await send_system_event_log(ctx,system_events)


async def send_system_event_log(ctx: discord.ApplicationContext, system_events: list):
    guildSettings = DataStorageManager.get_guild_settings(ctx.guild_id)
    
    if guildSettings.bgs_change_log_channel_id!=None:
        channel = bot.get_channel(guildSettings.bgs_change_log_channel_id)

        for system_event in system_events:
            view = None
            match system_event.event_type:
                case "MinorFactionJoinSystemEvent":
                    view = MinorFactionJoinSystemEventLogView(system_event)
                case "MinorFactionLeaveSystemEvent":
                    view = MinorFactionLeaveSystemEventLogView(system_event)
                case _:
                    view = None
            if view != None:
                await channel.send(embed=view.get_embed(), view=view)


@bot.slash_command(name="api_monitor", description="show status of each used apis", guild_ids=guildIDs)
async def api_monitor(ctx: discord.ApplicationContext):
    await ctx.defer()
    aPIStatus = APIManager.getAPIStatus()
    aPIMonitorView = APIMonitorView(aPIStatus)
    await ctx.edit(embed=aPIMonitorView.getEmbed(), view=aPIMonitorView)



@bot.slash_command(name="system_group", description="manage system groups: create group, edit group and delete group", guild_ids=guildIDs)
@PermissionManager.system_group_permissions.see_list_predicate()
async def system_group(ctx: discord.ApplicationContext):
    await ctx.defer()
    system_groups_view = SystemGroupsView(DataStorageManager.get_system_groups(ctx.guild_id))
    await ctx.edit(embed=system_groups_view.get_embed(), view=system_groups_view)



@bot.slash_command(name="system", description="show system information", guild_ids=guildIDs)
async def system(ctx: discord.ApplicationContext, system_name: str):
    await ctx.defer()
    guild_settings = DataStorageManager.get_guild_settings(ctx.guild_id)
    system = DataStorageManager.get_system(ctx.guild_id, system_name.lower())
    if system != None:
        view = SystemView(system,guild_settings)
    else:
        system = DataManager.requestSystemData(system_name.lower())
        if system != None:
            if system.minor_faction_is_present(guild_settings.minor_faction_name):
                DataStorageManager.store_system(ctx.guild_id, system)
                print("Untracked System Added")
            view = SystemView(system,guild_settings)
        else:
            view = ErrorMessageView(f"System \"{system_name}\" not found.")
    await ctx.edit(embed=view.getEmbed(), view=view)


@bot.slash_command(name="minor_faction", description="show minor faction information", guild_ids=guildIDs)
async def minor_faction(ctx: discord.ApplicationContext, minor_faction_name: str):
    await ctx.defer()
    minor_faction = DataStorageManager.get_minor_faction(ctx.guild_id, minor_faction_name.lower())
    if minor_faction != None:
        view = MinorFactionView(minor_faction,ctx.guild_id)
    else:
        view = ErrorMessageView(f"Minor Faction \"{minor_faction_name}\" not found.")
    await ctx.edit(embed=view.getEmbed(), view=view)


@bot.slash_command(name="bgs_recap", description="send recap of bgs (minor faction and system) in set channel", guild_ids=guildIDs)
async def bgs_recap(ctx: discord.ApplicationContext):
    guildSettings = DataStorageManager.get_guild_settings(ctx.guild_id)
    minorFaction = await asyncio.to_thread(DataStorageManager.get_minor_faction, ctx.guild_id, guildSettings.minor_faction_name)
    
    if minorFaction!=None:
        systemsRecap = DataManager.getMinorFactionSystemsRecap(ctx.guild_id)
        systemGroups = DataStorageManager.get_system_groups(ctx.guild_id)
        systemsWithNoGroups = DataManager.getSystemNamesWithNoGroupList(ctx.guild_id)
        systemsRecapViews = SystemsRecapViews(systemsRecap,systemGroups,systemsWithNoGroups)

        ##### BGS Recap
        if guildSettings.bgs_system_recap_channel_id!=None:
            channel = bot.get_channel(guildSettings.bgs_system_recap_channel_id)
            await channel.purge(check=isBotMessage)
            #minor faction
            # minorFactionView = MinorFactionView(minorFaction)
            # await channel.send(embed=minorFactionView.getEmbed(), view=minorFactionView)
            #systems legend
            systemsRecapLegendView = SystemsRecapLegendView(minorFaction.name)
            await channel.send(embed=systemsRecapLegendView.getEmbed())
            #systems
            embeds = systemsRecapViews.getSystemsMinorFactionRecapEmbeds()
            for i in range(len(embeds)):
                await channel.send(embed=embeds[i])

        ##### warning Recap
        if guildSettings.bgs_warning_recap_channel_id!=None:
            channel = bot.get_channel(guildSettings.bgs_warning_recap_channel_id)
            await channel.purge(check=isBotMessage)
            #expansion
            expEmbeds = systemsRecapViews.getExpansionWarningSystemRecapEmbeds()
            for i in range(len(expEmbeds)):
                await channel.send(embed=expEmbeds[i])
            #influence margin warning
            influenceMarginWarningEmbedsAll = systemsRecapViews.getInfluenceMarginWarningSystemRecapEmbeds()
            for influenceMarginWarningEmbeds in influenceMarginWarningEmbedsAll.values():
                for i in range(len(influenceMarginWarningEmbeds)):
                    await channel.send(embed=influenceMarginWarningEmbeds[i])
            #conflicts
            conflictEmbeds = systemsRecapViews.getConflictSystemRecapEmbeds()
            for i in range(len(conflictEmbeds)):
                await channel.send(embed=conflictEmbeds[i])
            #retreat
            retreatEmbeds = systemsRecapViews.get_retreat_warning_system_recap_embeds()
            for i in range(len(retreatEmbeds)):
                await channel.send(embed=retreatEmbeds[i])
                
    #### Missions Recap
    if guildSettings.mission_recap_channel_id!=None:
        missions_recap_views = MissionsRecapViews(ctx.guild_id)

        channel = bot.get_channel(guildSettings.mission_recap_channel_id)
        await channel.purge(check=isBotMessage)

        #retreat mission
        retreat_embeds = missions_recap_views.get_retreat_minor_faction_from_system_missions_recap_embeds()
        for i in range(len(retreat_embeds)):
            await channel.send(embed=retreat_embeds[i])


@bot.slash_command(name="settings", description="show guild settings", guild_ids=guildIDs)
@PermissionManager.guild_settings_permissions.see_predicate()
async def settings(ctx: discord.ApplicationContext):
    guild_settings = DataStorageManager.get_guild_settings(ctx.guild_id)
    guild_settings_view = DefaultGuildSettingsView(guild_settings)

    await ctx.send_response(embed=guild_settings_view.getEmbed(), view=guild_settings_view,ephemeral=True)



## error handler
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("You don't have the permission to do this.",ephemeral=True)
    elif isinstance(error, discord.errors.CheckFailure):
        await ctx.respond("You don't have the permission to do this.",ephemeral=True)
    else:
        raise error

####################################################################

#run bot
bot.run(token)

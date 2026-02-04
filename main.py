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
from Discord.View.GuildSettingsView import GuildSettingsView

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

@bot.slash_command(name="init", description="init", guild_ids=guildIDs)
async def init(ctx: discord.ApplicationContext):
    await ctx.defer()
    if DataManager.initStorage(ctx.guild_id):
        await ctx.edit(content="Init")
    else:
        await ctx.edit(content="Already Init")


@bot.slash_command(name="forceupdatebgsdata", description="force the update of minor faction systems bgs data", guild_ids=guildIDs)
async def forceupdatebgsdata(ctx: discord.ApplicationContext):
    await ctx.defer()
    #print("!!! shortened for tests")
    await asyncio.to_thread(DataManager.updateSystemsList, ctx.guild_id)
    await asyncio.to_thread(DataManager.updateStoredSystemsBGSData, ctx.guild_id)
    await ctx.edit(content="Systems BGS Data Updated Successfully!")


@bot.slash_command(name="apimonitor", description="show status of each used apis", guild_ids=guildIDs)
async def apimonitor(ctx: discord.ApplicationContext):
    await ctx.defer()
    aPIStatus = APIManager.getAPIStatus()
    aPIMonitorView = APIMonitorView(aPIStatus)
    await ctx.edit(embed=aPIMonitorView.getEmbed(), view=aPIMonitorView)


#manage system group
@bot.slash_command(name="systemgroup", description="manage system group (create, add system to group)", guild_ids=guildIDs)
@PermissionManager.system_group_permissions.see_list_predicate()
async def managesystemgroup(ctx: discord.ApplicationContext):
    await ctx.defer()

    systemGroupsView = SystemGroupsView(DataManager.getSystemGroups(ctx.guild_id))

    await ctx.edit(embed=systemGroupsView.getEmbed(), view=systemGroupsView)



@bot.slash_command(name="system", description="show system information", guild_ids=guildIDs)
async def system(ctx: discord.ApplicationContext, system_name: str):
    await ctx.defer()

    guildSettings = DataManager.getGuildSettings(ctx.guild_id)
    system = DataManager.getSystem(ctx.guild_id, system_name.lower())
    if system != None:
        view = SystemView(system,guildSettings)
    else:
        system = DataManager.requestSystemData(system_name.lower())
        if system != None:
            if system.haveFaction(guildSettings.minorFactionName):
                DataStorageManager.addSystemToDataFile(ctx.guild_id, system)
                print("Untracked System Added")
            view = SystemView(system,guildSettings)
        else:
            view = ErrorMessageView(f"System \"{system_name}\" not found.")


    await ctx.edit(embed=view.getEmbed(), view=view)


@bot.slash_command(name="bgsrecap", description="send recap of bgs (minor faction and system) in set channel", guild_ids=guildIDs)
async def test(ctx: discord.ApplicationContext):
    guildSettings = DataManager.getGuildSettings(ctx.guild_id)
    minorFaction = await asyncio.to_thread(DataManager.getMinorFaction, ctx.guild_id, guildSettings.minorFactionName)
    
    if minorFaction!=None:
        systemsRecap = DataManager.getMinorFactionSystemsRecap(ctx.guild_id)
        systemGroups = DataManager.getSystemGroups(ctx.guild_id)
        systemsWithNoGroups = DataManager.getSystemNamesWithNoGroupList(ctx.guild_id)
        systemsRecapViews = SystemsRecapViews(systemsRecap,systemGroups,systemsWithNoGroups)

        ##### BGS Recap
        if guildSettings.bgsSystemRecapChannelID!=None:
            channel = bot.get_channel(guildSettings.bgsSystemRecapChannelID)
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
        if guildSettings.bgsWarningRecapChannelID!=None:
            channel = bot.get_channel(guildSettings.bgsWarningRecapChannelID)
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



@bot.slash_command(name="guild_settings", description="show guild settings", guild_ids=guildIDs)
@PermissionManager.guild_settings_permissions.see_predicate()
async def guild_settings(ctx: discord.ApplicationContext):
    guildSettings = DataStorageManager.getGuildSettings(ctx.guild_id)
    guildSettingsView = GuildSettingsView(guildSettings)

    await ctx.send_response(embed=guildSettingsView.getEmbed(), view=guildSettingsView)


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

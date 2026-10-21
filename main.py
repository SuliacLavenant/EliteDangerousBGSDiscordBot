import discord
from discord.ext import commands

#import logging
from dotenv import load_dotenv
import os
import asyncio
import traceback

#custom files
#from DataClass.GuildSettings import GuildSettings
import DataClass

from PermissionManager.PermissionManager import PermissionManager
from DataManager import DataManager
# from DataStorageManager import DataStorageManager
# from APIRequester.APIManager import APIManager

from Discord.View.ErrorMessageView import ErrorMessageView
from Discord.View.MinorFactionView import MinorFactionView
from Discord.View.Player.PlayerView import PlayerView
from Discord.View.Player.PlayerNotFoundView import PlayerNotFoundView
# from Discord.View.SquadronView import SquadronView
# from Discord.View.SquadronsView import SquadronsView
# from Discord.View.SquadronNotFoundView import SquadronNotFoundView
from Discord.View.SystemView import SystemView
from Discord.View.SystemRecap.SystemsRecapViews import SystemsRecapViews
from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
from Discord.View.SystemRecap.SystemRecapLegendView import SystemsRecapLegendView
# from Discord.View.SystemRecap.Warning.ExpansionWarningSystemsRecapView import ExpansionWarningSystemsRecapView
from Discord.View.GuildSettings.DefaultGuildSettingsView import DefaultGuildSettingsView
# from Discord.View.MissionsRecap.MissionsRecapViews import MissionsRecapViews
# from Discord.View.MissionsRecap.MissionRecapLegendView import MissionRecapLegendView

# from Discord.View.SystemEventLog.MinorFactionJoinSystemEventLogView import MinorFactionJoinSystemEventLogView
# from Discord.View.SystemEventLog.MinorFactionAcquireLeadershipSystemEventLogView import MinorFactionAcquireLeadershipSystemEventLogView
# from Discord.View.SystemEventLog.MinorFactionLeaveSystemEventLogView import MinorFactionLeaveSystemEventLogView
# from Discord.View.SystemEventLog.MinorFactionLoseLeadershipSystemEventLogView import MinorFactionLoseLeadershipSystemEventLogView



from DatabaseGateway.DatabaseGateway import DatabaseGateway



########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################

#from Discord.View.APIMonitorView import APIMonitorView

from BotConfig.BotConfig import BotConfig
BotConfig.load()


#Discord app token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

DatabaseGateway.setup(os.getenv("DB_USER"),os.getenv("DB_PW"),int(os.getenv("DB_PORT")),os.getenv("DB_NAME"))


BotConfig.contact_email = os.getenv("CONTACT_EMAIL")
print(BotConfig.contact_email)

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
# for guild_id in guildIDs:
#     DataStorageManager.create_missing_data_files(guild_id)

# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("discord.http").setLevel(logging.DEBUG)


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

#TODO only update tracked ones
# now update for all discords
@bot.slash_command(name="forceupdatebgsdata", description="force the update of minor faction systems bgs data", guild_ids=guildIDs)
async def forceupdatebgsdata(ctx: discord.ApplicationContext):
    await ctx.defer()
    system_events = await DataManager.update_systems_bgs_data(ctx.guild_id)
    await ctx.edit(content="Systems BGS Data Updated Successfully!")
    # await send_system_event_log(ctx,system_events) #TODO


# async def send_system_event_log(ctx: discord.ApplicationContext, system_events: list):
#     guildSettings = DataStorageManager.get_guild_settings(ctx.guild_id)
    
#     if guildSettings.bgs_change_log_channel_id!=None:
#         channel = bot.get_channel(guildSettings.bgs_change_log_channel_id)

#         for system_event in system_events:
#             view = None
#             match system_event.event_type:
#                 case "MinorFactionJoinSystemEvent":
#                     view = MinorFactionJoinSystemEventLogView(system_event)
#                 case "MinorFactionLeaveSystemEvent":
#                     view = MinorFactionLeaveSystemEventLogView(system_event)
#                 case "MinorFactionLoseLeadershipSystemEvent":
#                     view = MinorFactionLoseLeadershipSystemEventLogView(system_event)
#                 case "MinorFactionAcquireLeadershipSystemEvent":
#                     view = MinorFactionAcquireLeadershipSystemEventLogView(system_event)
#                 case _:
#                     view = None
#             if view != None:
#                 await channel.send(embed=view.get_embed(), view=view)


# @bot.slash_command(name="api_monitor", description="show status of each used apis", guild_ids=guildIDs)
# async def api_monitor(ctx: discord.ApplicationContext):
#     await ctx.defer()
#     aPIStatus = APIManager.getAPIStatus()
#     aPIMonitorView = APIMonitorView(aPIStatus)
#     await ctx.edit(embed=aPIMonitorView.getEmbed(), view=aPIMonitorView)



@bot.slash_command(name="system_group", description="manage system groups: create group, edit group and delete group", guild_ids=guildIDs)
@PermissionManager.system_group_permissions.see_list_predicate()
async def system_group(ctx: discord.ApplicationContext):
    await ctx.defer()
    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(ctx.guild_id)
    system_groups: list = await DatabaseGateway.system_group.get_all_from_discord(guild_settings.id)
    system_groups_view: SystemGroupsView = SystemGroupsView(system_groups, guild_settings)
    await ctx.edit(embed=system_groups_view.get_embed(), view=system_groups_view)



@bot.slash_command(name="system", description="show system information", guild_ids=guildIDs)
async def system(ctx: discord.ApplicationContext, system_name: str):
    await ctx.defer()
    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(ctx.guild_id)
    system: System = await DatabaseGateway.system.get_by_name(system_name, True)
    if system != None:
        is_system_tracked_by_discord: bool = await DatabaseGateway.discord_tracked_system.exists(guild_settings.id, system.id)
        view = SystemView(system, guild_settings, is_system_tracked_by_discord, guild_settings.is_channel_trusted(ctx.channel_id))
        await ctx.edit(embeds=view.get_embeds(), view=view)
    else:
        system = await DataManager.request_and_store_system_data(system_name.lower())
        if system != None:
            # if system.minor_faction_is_present(guild_settings.minor_faction_name):
            #     # DataStorageManager.store_system(ctx.guild_id, system)
            #     await DatabaseGateway.system.add(system)
            #     print("Untracked System Added")
            system = await DatabaseGateway.system.get_by_name(system_name, True)
            is_system_tracked_by_discord: bool = await DatabaseGateway.discord_tracked_system.exists(guild_settings.id, system.id)
            view = SystemView(system, guild_settings, is_system_tracked_by_discord, guild_settings.is_channel_trusted(ctx.channel_id))
            await ctx.edit(embeds=view.get_embeds(), view=view)
        else:
            view = ErrorMessageView(f"System \"{system_name}\" not found.")
            await ctx.edit(embed=view.get_embed(), view=view)


@bot.slash_command(name="minor_faction", description="show minor faction information", guild_ids=guildIDs)
async def minor_faction(ctx: discord.ApplicationContext, minor_faction_name: str):
    await ctx.defer()
    minor_faction: MinorFaction = await DatabaseGateway.minor_faction.get_by_name(minor_faction_name.lower())
    if minor_faction != None:
        view = MinorFactionView(minor_faction,ctx.guild_id)
    else:
        view = ErrorMessageView(f"Minor Faction \"{minor_faction_name}\" not found.")
    await ctx.edit(embed=view.get_embed(), view=view)

#-----------------> working here TODO
@bot.slash_command(name="bgs_recap", description="send recap of bgs (minor faction and system) in set channel", guild_ids=guildIDs)
async def bgs_recap(ctx: discord.ApplicationContext):
    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(ctx.guild_id)

    # minorFaction = await asyncio.to_thread(DataStorageManager.get_minor_faction, ctx.guild_id, guildSettings.minor_faction_name) <----

    if guild_settings.minor_faction_id != None:
        guild_settings = await DatabaseGateway.guild_settings.get(guild_settings.id, True, True, True)

        system_recaps = DataManager.get_minor_faction_tracked_system_recaps(guild_settings.tracked_systems, guild_settings.minor_faction)
        
        system_names_with_no_groups = guild_settings.get_tracked_system_names_with_no_group()
        systems_recap_views: SystemsRecapViews = SystemsRecapViews(guild_settings, system_recaps, guild_settings.system_groups, system_names_with_no_groups)

        ##### BGS Recap
        if guild_settings.bgs_system_recap_channel_id is not None:
            channel = bot.get_channel(guild_settings.bgs_system_recap_channel_id)
            await channel.purge(check=isBotMessage)
            #minor faction
            # minorFactionView = MinorFactionView(minorFaction)
            # await channel.send(embed=minorFactionView.getEmbed(), view=minorFactionView)
            #systems legend
            systems_recap_legend_view = SystemsRecapLegendView(guild_settings.minor_faction.name)
            await channel.send(embed=systems_recap_legend_view.get_embed())
            #systems
            embeds = systems_recap_views.get_systems_minor_faction_recap_embeds()
            for i, embed in enumerate(embeds):
                print(f"Sending embed {i+1}/{len(embeds)}", flush=True)
                message = await channel.send(embed=embed)
                print(f"Sent: {message.id}", flush=True)
                await asyncio.sleep(0.5)

        ##### warning Recap
        if guild_settings.bgs_warning_recap_channel_id!=None:
            channel = bot.get_channel(guild_settings.bgs_warning_recap_channel_id)
            await channel.purge(check=isBotMessage)
            #expansion
            expEmbeds: list[discord.Embed] = systems_recap_views.get_expansion_warning_system_recap_embeds()
            for i in range(len(expEmbeds)):
                await channel.send(embed=expEmbeds[i])
            #influence margin warning
            influence_margin_warning_embeds_all: list[discord.Embed] = systems_recap_views.get_influence_margin_warning_system_recap_embeds()
            for influence_margin_warning_embeds in influence_margin_warning_embeds_all.values():
                for i in range(len(influence_margin_warning_embeds)):
                    await channel.send(embed=influence_margin_warning_embeds[i])
            #conflicts
            conflictEmbeds: list[discord.Embed] = systems_recap_views.get_conflict_system_recap_embeds()
            for i in range(len(conflictEmbeds)):
                await channel.send(embed=conflictEmbeds[i])
            #retreat
            retreatEmbeds: list[discord.Embed] = systems_recap_views.get_retreat_warning_system_recap_embeds()
            for i in range(len(retreatEmbeds)):
                await channel.send(embed=retreatEmbeds[i])
        
#     await update_mission_recaps(ctx.guild_id)


# async def update_mission_recaps(guild_id: int):
#     guild_settings = DataStorageManager.get_guild_settings(guild_id)
#     #### Missions Recap
#     if guild_settings.mission_recap_channel_id!=None:
#         missions_recap_views = MissionsRecapViews(guild_id)

#         channel = bot.get_channel(guild_settings.mission_recap_channel_id)
#         await channel.purge(check=isBotMessage)

#         ##### Legend
#         mission_recap_legend_view = MissionRecapLegendView()
#         await channel.send(embed=mission_recap_legend_view.get_embed())

#         # retreat_embeds = missions_recap_views.get_retreat_minor_faction_from_system_missions_recap_embeds()
#         # for i in range(len(retreat_embeds)):
#         #     await channel.send(embed=retreat_embeds[i])
#         # set_leader_embeds = missions_recap_views.get_set_minor_faction_as_leader_in_system_missions_recap_embeds()
#         # for i in range(len(set_leader_embeds)):
#         #     await channel.send(embed=set_leader_embeds[i])

#         system_missions_views = missions_recap_views.get_missions_recap_per_system_views()
#         for system_missions_view in system_missions_views:
#             await channel.send(embed=system_missions_view.get_embed_short(), view=system_missions_view)


@bot.slash_command(name="settings", description="show guild settings", guild_ids=guildIDs)
@PermissionManager.guild_settings_permissions.see_predicate()
async def settings(ctx: discord.ApplicationContext):
    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(ctx.guild_id)
    guild_settings_view: DefaultGuildSettingsView = DefaultGuildSettingsView(guild_settings)

    await ctx.send_response(embed=guild_settings_view.get_embed(), view=guild_settings_view)


# @bot.slash_command(name="squadron", description="show squadron information", guild_ids=guildIDs)
# @PermissionManager.squadron_permissions.see_predicate()
# async def squadron(ctx: discord.ApplicationContext, squadron_name: str):
#     await ctx.defer()
#     squadron = DataStorageManager.get_squadron_by_name(ctx.guild_id, squadron_name)
#     if squadron == None:
#         squadron_not_found_view = SquadronNotFoundView(squadron_name, ctx.guild_id)
#         await ctx.edit(embed=squadron_not_found_view.get_embed(), view=squadron_not_found_view)
#     else:
#         squadron_view = SquadronView(squadron, ctx.guild_id)
#         await ctx.edit(embed=squadron_view.get_embed(), view=squadron_view)


# @bot.slash_command(name="squadrons", description="show stored squadrons", guild_ids=guildIDs)
# @PermissionManager.squadron_permissions.see_list_predicate()
# async def squadrons(ctx: discord.ApplicationContext):
#     await ctx.defer()
#     squadrons: list[Squadron] = DataStorageManager.get_squadrons(ctx.guild_id)
#     squadrons_view = SquadronsView(squadrons, ctx.guild_id)
#     await ctx.edit(embed=squadrons_view.get_embed(), view=squadrons_view)


@bot.slash_command(name="player", description="show player information", guild_ids=guildIDs)
@PermissionManager.player_permissions.see_predicate()
async def player(ctx: discord.ApplicationContext, player_name: str):
    await ctx.defer()
    # player = DataStorageManager.get_player_by_name(ctx.guild_id, player_name)
    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(ctx.guild_id)
    player: Player = await DatabaseGateway.player.get(guild_settings.id, player_name)
    if player == None:
        player_not_found_view: PlayerNotFoundView = PlayerNotFoundView(player_name, guild_settings.id)
        await ctx.edit(embed=player_not_found_view.get_embed(), view=player_not_found_view)
    else:
        player_view = PlayerView(player, guild_settings.id)
        await ctx.edit(embeds=player_view.get_embeds(), view=player_view)



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
async def main():
    try:
        await bot.start(token)
    finally:
        if not bot.is_closed():
            await bot.close()


if __name__ == "__main__":
    try:
        asyncio.run(
            main(),
            loop_factory=asyncio.SelectorEventLoop
        )
    except KeyboardInterrupt:
        pass

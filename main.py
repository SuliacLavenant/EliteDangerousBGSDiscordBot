import discord
from discord.ext import commands

#import logging
from dotenv import load_dotenv
import os
import asyncio

#custom files
from DataClass.GuildSettings import GuildSettings

from DataManager import DataManager
from DataProcessor import DataProcessor
from APIRequester.APIManager import APIManager

from Discord.View.ErrorMessageView import ErrorMessageView
from Discord.View.MinorFactionView import MinorFactionView
from Discord.View.SystemView import SystemView
from Discord.View.SystemRecap.SystemsRecapViews import SystemsRecapViews
from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
from Discord.View.SystemRecap.SystemRecapLegendView import SystemsRecapLegendView

from Discord.View.APIMonitorView import APIMonitorView

from BotConfig.BotConfig import BotConfig
BotConfig.load()


#Discord app token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

guildIDs_raw = os.getenv("DISCORD_GUILDS")
guildIDs = [int(guildID) for guildID in guildIDs_raw.split(",") if guildID]
print(guildIDs)
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
async def managesystemgroup(ctx: discord.ApplicationContext):
    await ctx.defer()

    systemGroupsView = SystemGroupsView(DataManager.getSystemGroups(ctx.guild_id))

    await ctx.edit(embed=systemGroupsView.getEmbed(), view=systemGroupsView)



@bot.slash_command(name="system", description="show system information", guild_ids=guildIDs)
async def system(ctx: discord.ApplicationContext, system_name: str):
    await ctx.defer()

    system = DataManager.getSystem(ctx.guild_id, system_name.lower())
    if system != None:
        view = SystemView(system)
    else:
        view = ErrorMessageView("System not found in Minor Faction systems")


    await ctx.edit(embed=view.getEmbed(), view=view)


@bot.slash_command(name="bgsrecap", description="send recap of bgs (minor faction and system) in set channel", guild_ids=guildIDs)
async def test(ctx: discord.ApplicationContext):
    guildSettings = DataManager.getGuildSettings(ctx.guild_id)
    channel = bot.get_channel(guildSettings.bgsRecapChanelID)

    #purge du chanel
    await channel.purge(check=isBotMessage)

    minorFactionName = DataManager.getGuildMinorFactionName(ctx.guild_id)
    minorFaction = await asyncio.to_thread(DataManager.getMinorFaction, ctx.guild_id, minorFactionName)
    minorFactionView = MinorFactionView(minorFaction)

    if minorFaction!=None:
        systemsRecapLegendView = SystemsRecapLegendView(minorFaction.name)

        systemsRecap = await asyncio.to_thread(DataProcessor.getMinorFactionSystemsRecap, ctx.guild_id)
        systemGroups = await asyncio.to_thread(DataManager.getSystemGroups, ctx.guild_id)
        systemsWithNoGroups = await asyncio.to_thread(DataManager.getSystemNamesWithNoGroupList, ctx.guild_id)
        embeds = SystemsRecapViews.getSystemsMinorFactionRecapEmbeds(systemsRecap,systemGroups,systemsWithNoGroups)
    
    #Send Messages
    await channel.send(embed=minorFactionView.getEmbed(), view=minorFactionView)
    if minorFaction!=None:
        await channel.send(embed=systemsRecapLegendView.getEmbed())
        for i in range(len(embeds)):
            await channel.send(embed=embeds[i])


@bot.slash_command(name="setbgsrecapchanel", description="test", guild_ids=guildIDs)
async def setbgsrecapchanel(ctx: discord.ApplicationContext):
    guildSettings = DataManager.getGuildSettings(ctx.guild_id)
    guildSettings.bgsRecapChanelID = ctx.channel_id
    DataManager.saveGuildSettings(ctx.guild_id, guildSettings)

    await ctx.send_response("BGS recap chanel succesfully set!", ephemeral=True)


####################################################################

#run bot
bot.run(token)

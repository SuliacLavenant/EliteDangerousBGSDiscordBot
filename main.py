import discord
from discord.ext import commands

#import logging
from dotenv import load_dotenv
import os
import asyncio

#custom files
from DataManager import DataManager
from DataProcessor import DataProcessor
from APIRequester.APIManager import APIManager

from View.MinorFactionView import MinorFactionView
from View.SystemsRecapViews import SystemsRecapViews
from View.SystemGroup.ManageSystemGroupView import ManageSystemGroupView

from Discord.View.APIMonitorView import APIMonitorView

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
    await asyncio.to_thread(DataManager.updateSystemsBGSData, ctx.guild_id)
    await ctx.edit(content="Systems BGS Data Updated Successfully!")


@bot.slash_command(name="minorfaction", description="show info on minor faction", guild_ids=guildIDs)
async def minorfaction(ctx: discord.ApplicationContext):
    await ctx.defer()
    minorFaction = await asyncio.to_thread(DataManager.getMinorFaction, ctx.guild_id)
    minorFactionView = MinorFactionView(minorFaction)
    await ctx.edit(embed=minorFactionView.getEmbed(), view=minorFactionView)


#get systems info recap
@bot.slash_command(name="getsystemsrecap", description="show info on systems", guild_ids=guildIDs)
async def getsystemsrecap(ctx: discord.ApplicationContext):
    await ctx.defer(ephemeral=True)

    systemsRecap = await asyncio.to_thread(DataProcessor.getMinorFactionSystemsRecap, ctx.guild_id)
    embeds = SystemsRecapViews.getRawSystemsMinorFactionRecapEmbeds(systemsRecap)
    
    #edit original message
    await ctx.edit(content="Done")

    #send embeds to discords
    for i in range(len(embeds)):
        await ctx.channel.send(embed=embeds[i])

    #text answer
    # sytemsRecapStr = ""
    # for systemRecap in systemsRecap:
    #     sytemsRecapStr = sytemsRecapStr + systemRecap.__str__() + "\n"
    # await interaction.edit_original_response(content=sytemsRecapStr)


@bot.slash_command(name="apimonitor", description="show status of each used apis", guild_ids=guildIDs)
async def apimonitor(ctx: discord.ApplicationContext):
    await ctx.defer()
    aPIStatus = APIManager.getAPIStatus()
    aPIMonitorView = APIMonitorView(aPIStatus)
    await ctx.edit(embed=aPIMonitorView.getEmbed(), view=aPIMonitorView)


#manage system group
@bot.slash_command(name="managesystemgroup", description="manage system group (create, add system to group)", guild_ids=guildIDs)
async def managesystemgroup(ctx: discord.ApplicationContext):
    await ctx.defer()

    manageSystemGroupView = ManageSystemGroupView(DataManager.getSystemGroups(ctx.guild_id))

    await ctx.edit(embed=manageSystemGroupView.getEmbed(), view=manageSystemGroupView)

####################################################################

#run bot
bot.run(token)

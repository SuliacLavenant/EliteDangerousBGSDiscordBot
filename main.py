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
from View.APIStatusView import APIStatusView
from View.SystemGroup.ManageSystemGroupView import ManageSystemGroupView

#Discord app token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guildID = int(os.getenv("DISCORD_GUILD"))

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

#Set minor faction for the discord
#TODO restrict permission + confirmation to reset if already set
@bot.slash_command(name="setminorfaction", description="set the minor faction for this discord", guild_ids=[guildID])
async def setminorfaction(interaction: discord.Interaction, minorfactionname: str):
    if DataManager.setPlayerMinorFaction(interaction.guild_id,minorfactionname):
        await interaction.response.send_message(f"Minor Faction \"{minorfactionname.lower().title()}\" Successfully set!")
    else:
        await interaction.response.send_message(f"cannot find \"{minorfactionname.lower().title()}\" Minor Faction. This can happen if the faction does not exist, if it is a recent addition, or if the API has not responded.")


@bot.slash_command(name="forceupdatebgsdata", description="force the update of minor faction systems bgs data", guild_ids=[guildID])
async def forceupdatebgsdata(ctx: discord.ApplicationContext):
    await ctx.defer()
    await asyncio.to_thread(DataManager.updateSystemsBGSData, ctx.guild_id)
    await ctx.edit(content="Systems BGS Data Updated Successfully!")


#get faction info recap
@bot.slash_command(name="getminorfactioninfo", description="show info on minor faction", guild_ids=[guildID])
async def getminorfactioninfo(ctx: discord.ApplicationContext):
    await ctx.defer()

    minorFaction = await asyncio.to_thread(DataManager.getMinorFaction, ctx.guild_id)
    minorFactionView = MinorFactionView(minorFaction)

    #embed answer
    await ctx.edit(embed=minorFactionView.getEmbed(), view=minorFactionView)

    #text answer
    #await interaction.edit_original_response(content=minorFaction)


#get systems info recap
@bot.slash_command(name="getsystemsrecap", description="show info on systems", guild_ids=[guildID])
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


#get api status
@bot.slash_command(name="apistatus", description="show status of each used apis", guild_ids=[guildID])
async def apistatus(ctx: discord.ApplicationContext):
    await ctx.defer()
    aPIStatus = APIManager.getAPIStatus()
    aPIStatusView = APIStatusView(aPIStatus)
    await ctx.edit(embed=aPIStatusView.getEmbed(), view=aPIStatusView)


#manage system group
@bot.slash_command(name="managesystemgroup", description="manage system group (create, add system to group)", guild_ids=[guildID])
async def managesystemgroup(ctx: discord.ApplicationContext):
    await ctx.defer()

    manageSystemGroupView = ManageSystemGroupView(DataManager.getSystemGroups(ctx.guild_id))

    await ctx.edit(embed=manageSystemGroupView.getEmbed(), view=manageSystemGroupView)

####################################################################

#run bot
bot.run(token)

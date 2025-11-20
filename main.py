import discord
from discord.ext import commands
from discord import app_commands
#import logging
from dotenv import load_dotenv
import os
import asyncio

#custom files
from BGSManagementBot import BGSManagementBot
from APIRequester.EliteBGSAPIAPIRequester import EliteBGSAPIAPIRequester
from SystemInfoMinorFactionFocused import SystemInfoMinorFactionFocused

from DataManager import DataManager
from DataProcessor import DataProcessor
from APIRequester.APIManager import APIManager

from View.MinorFactionView import MinorFactionView
from View.SystemsRecapView import SystemsRecapView
from View.APIStatusView import APIStatusView
from View.SystemGroup.ManageSystemGroupView import ManageSystemGroupView

#Discord app token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guildID = os.getenv("DISCORD_GUILD")

#Intents for discord
intents = discord.Intents.default()
intents.message_content = True

#create bot
bot = BGSManagementBot(command_prefix=".", intents=intents)

guild = discord.Object(id=guildID)

####################################################################

#Set minor faction for the discord
#TODO restrict permission + confirmation to reset if already set
@bot.tree.command(name="setminorfaction", description="set the minor faction for this discord", guild=guild)
async def setminorfaction(interaction: discord.Interaction, minorfactionname: str):
    print(interaction.guild_id)
    if DataManager.setPlayerMinorFaction(interaction.guild_id,minorfactionname):
        await interaction.response.send_message(f"Minor Faction \"{minorfactionname.lower().title()}\" Successfully set!")
    else:
        await interaction.response.send_message(f"cannot find \"{minorfactionname.lower().title()}\" Minor Faction. This can happen if the faction does not exist, if it is a recent addition, or if the API has not responded.")

#force update systems BGS data
@bot.tree.command(name="forceupdatebgsdata", description="force the update of minor faction systems bgs data", guild=guild)
async def forceupdatebgsdata(interaction: discord.Interaction):
    print(interaction.guild_id)
    await interaction.response.defer(thinking=True)

    await asyncio.to_thread(DataManager.updateSystemsBGSData, interaction.guild_id)

    await interaction.edit_original_response(
        content="Systems BGS Data Updated Successfully!"
    )


#get faction info recap
@bot.tree.command(name="getminorfactioninfo", description="show info on minor faction", guild=guild)
async def getminorfactioninfo(interaction: discord.Interaction):
    print(interaction.guild_id)
    await interaction.response.defer(thinking=True)

    minorFaction = await asyncio.to_thread(DataManager.getMinorFaction, interaction.guild_id)
    minorFactionView = MinorFactionView(minorFaction)

    #embed answer
    await interaction.edit_original_response(embed=minorFactionView.getEmbed(), view=minorFactionView)

    #text answer
    #await interaction.edit_original_response(content=minorFaction)


#get systems info recap
@bot.tree.command(name="getsystemsrecap", description="show info on systems", guild=guild)
async def getsystemsrecap(interaction: discord.Interaction):
    print(interaction.guild_id)
    await interaction.response.defer(thinking=True,ephemeral=True)

    systemsRecap = await asyncio.to_thread(DataProcessor.getMinorFactionSystemsRecap, interaction.guild_id)
    embeds = bot.getRawSystemsMinorFactionRecapEmbeds(systemsRecap)
    
    #edit original message
    await interaction.edit_original_response(content="Done")

    #send embeds to discords
    for i in range(len(embeds)):
        await interaction.channel.send(embed=embeds[i])

    #text answer
    # sytemsRecapStr = ""
    # for systemRecap in systemsRecap:
    #     sytemsRecapStr = sytemsRecapStr + systemRecap.__str__() + "\n"
    # await interaction.edit_original_response(content=sytemsRecapStr)


#get api status
@bot.tree.command(name="apistatus", description="show status of each used apis", guild=guild)
async def apistatus(interaction: discord.Interaction):
    print(interaction.guild_id)
    await interaction.response.defer(thinking=True)

    aPIStatus = APIManager.getAPIStatus()
    aPIStatusView = APIStatusView(aPIStatus)

    await interaction.edit_original_response(embed=aPIStatusView.getEmbed(), view=aPIStatusView)


#manage system group
@bot.tree.command(name="managesystemgroup", description="manage system group (create, add system to group)", guild=guild)
async def managesystemgroup(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    manageSystemGroupView = ManageSystemGroupView(DataManager.getSystemGroups(interaction.guild_id))

    await interaction.edit_original_response(embed=manageSystemGroupView.getEmbed(), view=manageSystemGroupView)

####################################################################

@bot.tree.command(name="hello", description="say Hello World", guild=guild)
async def helloworld(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

@bot.tree.command(name="helloworldparameter", description="say Hello World with other world", guild=guild)
async def helloworldparameter(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(f"Helloo World! {word}")




#run bot
bot.run(token)

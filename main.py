import discord
from discord.ext import commands
from discord import app_commands
#import logging
from dotenv import load_dotenv
import os

#custom files
from BGSManagementBot import BGSManagementBot
from APIRequester.EliteBGSAPIAPIRequester import EliteBGSAPIAPIRequester
from SystemInfoMinorFactionFocused import SystemInfoMinorFactionFocused

from DataManager import DataManager

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



####################################################################

@bot.tree.command(name="hello", description="say Hello World", guild=guild)
async def helloworld(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

@bot.tree.command(name="helloworldparameter", description="say Hello World with other world", guild=guild)
async def helloworldparameter(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(f"Helloo World! {word}")

@bot.tree.command(name="getsystemrecap", description="send an embed contenant a recap of the requested system", guild=guild)
async def getsystemrecap(interaction: discord.Interaction, systemname: str):
    systemInfoMinorFaction = EliteBGSAPIAPIRequester.requestSystemFactionData(systemname, "Empire Corsairs")
    await interaction.response.send_message(embed=bot.getSystemMinorFactionRecapEmbed(systemInfoMinorFaction))



#run bot
bot.run(token)

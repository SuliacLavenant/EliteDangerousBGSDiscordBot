import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from DataClass.System import System
from DataClass.GuildSettings import GuildSettings

from Discord.Modal.System.SetSystemArchitectModal import SetSystemArchitectModal

class SystemView(discord.ui.View):
    def __init__(self, system: System, guildSettings: GuildSettings):
        super().__init__()
        self.system = system
        self.guildSettings = guildSettings

        
        self.add_item(discord.ui.Button(
            label="Inara",
            url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system.name)}",
            emoji="🌐",
            row=0
        ))

        if self.system.isStored:
            if self.system.isArchitected == None:
                setArchitectButton = discord.ui.Button(
                    label="Set Architect",
                    style=discord.ButtonStyle.secondary,
                    emoji="🏗️",
                    row=1
                )
                setArchitectButton.callback = self.setArchitectButtonCallback
                self.add_item(setArchitectButton)

                setNativeSystemtButton = discord.ui.Button(
                    label="Native System",
                    style=discord.ButtonStyle.secondary,
                    emoji="🏛️",
                    row=1
                )
                setNativeSystemtButton.callback = self.setNativeSystemtButtonCallback
                self.add_item(setNativeSystemtButton)


    async def setArchitectButtonCallback(self, interaction: discord.Interaction):
        setSystemArchitectModal = SetSystemArchitectModal(self.system)
        await interaction.response.send_modal(setSystemArchitectModal)
        await setSystemArchitectModal.wait()

        system = DataManager.getSystem(interaction.guild_id,self.system.name)
        systemView = SystemView(system, self.guildSettings)
        await interaction.edit_original_response(view=systemView,embed=systemView.getEmbed())


    async def setNativeSystemtButtonCallback(self, interaction: discord.Interaction):
        system = DataManager.getSystem(interaction.guild_id,self.system.name)
        system.isArchitected = False

        DataStorageManager.updateSystem(interaction.guild_id,system)

        systemView = SystemView(system, self.guildSettings)
        await interaction.response.edit_message(view=systemView,embed=systemView.getEmbed())



    def getEmbed(self):
        title = self.system.name.title()
        if self.system.isStored:
            title += f" {BotConfig.emotesN.data.saved}"
        else:
            title += f" {BotConfig.emotesN.data.online}"

        description = f"{BotConfig.emotesN.system.information.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotesN.system.information.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotesN.system.information.security} Security Level: **{self.system.security.title()}**\n"
        if self.system.isArchitected:
            description += f"{BotConfig.emotesN.system.information.architect} Architect: **{self.system.architect.title()}**\n"
        description += "."

        embed = discord.Embed(title=title, description=description)

        ranking = self.system.getMinorFactionsRanking()
        current = 1
        while current<=len(ranking):
            minorFactionDict = self.system.factions[ranking[current]]
            minorFactionDescription = f"Allegiance: **{minorFactionDict["allegiance"].title()}**\n"
            minorFactionDescription += f"Government: **{minorFactionDict["government"].title()}**\n"

            emote = ""
            if current == 1:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.leader
            else:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.other

            title = f"{emote} {minorFactionDict["name"].title()} {emote} - < {round(minorFactionDict["influence"]*100,1)}% >"
            if minorFactionDict["name"] == self.guildSettings.minorFactionName:
                title += f" {BotConfig.emotesN.pin}"

            embed.add_field(name=title, value=minorFactionDescription, inline=False)

            current+=1

        return embed
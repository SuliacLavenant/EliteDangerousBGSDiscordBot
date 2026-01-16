import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from DataClass.System import System
from Discord.Modal.System.SetSystemArchitectModal import SetSystemArchitectModal

class SystemView(discord.ui.View):
    def __init__(self, system: System, isInStorage: bool = False):
        super().__init__()
        self.system = system

        
        self.add_item(discord.ui.Button(
            label="Inara",
            url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system.name)}",
            emoji="🌐",
            row=0
        ))


    @discord.ui.button(label="Set Architect", style=discord.ButtonStyle.secondary, emoji="🏗️", row=1)
    async def setMinorFaction(self, button: discord.ui.Button, interaction: discord.Interaction):
        setSystemArchitectModal = SetSystemArchitectModal(self.system)
        await interaction.response.send_modal(setSystemArchitectModal)
        await setSystemArchitectModal.wait()

        system = DataManager.getSystem(interaction.guild_id,self.system.name)
        systemView = SystemView(system)
        await interaction.edit_original_response(view=systemView,embed=systemView.getEmbed())



    def getEmbed(self):
        title = self.system.name.title()
        if self.system.isStored:
            title += f" {BotConfig.emotesN.data.saved}"
        else:
            title += f" {BotConfig.emotesN.data.online}"

        description = f"{BotConfig.emotesN.system.information.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotesN.system.information.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotesN.system.information.security} Security Level: **{self.system.security.title()}**\n"
        if self.system.architect != "":
            description += f"{BotConfig.emotesN.system.information.architect} Architect: **{self.system.architect.title()}**\n"
        description += "."

        embed = discord.Embed(title=title, description=description)

        ranking = self.system.getMinorFactionsRanking()
        current = 1
        while current<=len(ranking):
            emote = ""
            if current == 1:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.leader
            else:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.other
            minorFactionDict = self.system.factions[ranking[current]]
            minorFactionDescription = f"Allegiance: **{minorFactionDict["allegiance"].title()}**\n"
            minorFactionDescription += f"Government: **{minorFactionDict["government"].title()}**\n"
            embed.add_field(name=f"{emote} {minorFactionDict["name"].title()} {emote} - < {round(minorFactionDict["influence"]*100,1)}% >", value=minorFactionDescription, inline=False)

            current+=1

        return embed
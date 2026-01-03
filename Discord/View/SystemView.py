import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataClass.System import System

class SystemView(discord.ui.View):
    def __init__(self, system: System):
        super().__init__()
        self.system = system

        if self.system != None:
            self.add_item(discord.ui.Button(
                label="Inara",
                url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(system.name)}",
                emoji="🌐"
            ))


    def getEmbed(self):
        title = self.system.name.title()
        description = f"{BotConfig.emotesN.systemInformation.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotesN.systemInformation.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotesN.systemInformation.security} Security Level: **{self.system.security.title()}**\n"
        if self.system.architect != "":
            description += f"{BotConfig.emotesN.systemInformation.architect} Architect: **{self.system.architect.title()}**\n"
        description += "."

        embed = discord.Embed(title=title, description=description)

        controllingFactionDict = self.system.factions[self.system.controllingFactionName]
        controllingFactionDescription = f"Name: **{controllingFactionDict["name"].title()}**\n"
        controllingFactionDescription += f"Allegiance: **{controllingFactionDict["allegiance"].title()}**\n"
        controllingFactionDescription += f"Government: **{controllingFactionDict["government"].title()}**\n"

        embed.add_field(name=f"{BotConfig.positionInSystemEmotes["leader"]} Controlling Faction {BotConfig.positionInSystemEmotes["leader"]}", value=controllingFactionDescription, inline=False)

        return embed

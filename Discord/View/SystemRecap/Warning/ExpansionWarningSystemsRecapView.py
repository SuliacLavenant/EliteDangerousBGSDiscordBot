import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class ExpansionWarningSystemsRecapView(SystemsRecapView):
    title: str = "Expansion Warning"

    def __init__(self, systemsRecap: dict, isTitle: bool = False):
        super().__init__(systemsRecap, None, self.title)
        self.isTitle = isTitle


    def getEmbed(self):
        description=""
        i=0
        for systemRecap in self.systemsRecap.values():
            description += self.getSystemRecapOneLine(systemRecap)
            description += "\n"
            i+=1
            if i>15:
                break

        if self.isTitle:
            embed = discord.Embed(title=self.title, description=description, color=discord.Color.blue())
        else:
            embed = discord.Embed(title="", description=description, color=discord.Color.blue())

        return embed


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{BotConfig.emotes["warningExpansion"]} | {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | **< {round(systemRecap.influence*100,1)} % >** {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

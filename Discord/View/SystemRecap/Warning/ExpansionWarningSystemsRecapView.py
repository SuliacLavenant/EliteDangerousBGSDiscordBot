import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class ExpansionWarningSystemsRecapView(SystemsRecapView):
    def __init__(self, systemsRecapDict: dict, isTitle: bool = False):
        super().__init__(systemsRecapDict)
        self.isTitle = isTitle
        self.color = discord.Color.blue()

        if isTitle:
            self.title = f"{BotConfig.emotesN.minorFaction.state.expansion} Expansion Warning {BotConfig.emotesN.minorFaction.state.expansion}"


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)} {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

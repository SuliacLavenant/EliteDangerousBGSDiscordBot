import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class RetreatWarningSystemsRecapView(SystemsRecapView):
    def __init__(self, systemsRecapDict: dict, isTitle: bool = False):
        super().__init__(systemsRecapDict)
        self.isTitle = isTitle
        self.color = discord.Color.red()

        if isTitle:
            self.title = f"{BotConfig.emotesN.minorFaction.state.retreat} Retreat Warning {BotConfig.emotesN.minorFaction.state.retreat} (retreat warning: {round(BotConfig.bgs.state.retreat.warning_influence*100,1)}%, retreat trigger: {round(BotConfig.bgs.state.retreat.trigger_influence*100,1)}%)"


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getImportantStatusEmote(systemRecap)} | {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)} {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

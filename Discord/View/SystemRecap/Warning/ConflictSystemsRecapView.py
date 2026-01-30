import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class ConflictSystemsRecapView(SystemsRecapView):
    def __init__(self, systemsRecapDict: dict, isTitle: bool = False):
        super().__init__(systemsRecapDict)
        self.isTitle = isTitle
        self.color = discord.Color.red()

        if isTitle:
            self.title = f"{BotConfig.emotesN.minorFaction.state.war}{BotConfig.emotesN.minorFaction.state.election} Conflicts (War and Election) {BotConfig.emotesN.minorFaction.state.election}{BotConfig.emotesN.minorFaction.state.war}"


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getImportantStatusEmote(systemRecap)} | {self.getPositionEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class GeneralSystemsRecapView(SystemsRecapView):
    def __init__(self, systemsRecapDict: dict, color: discord.Color = None, title: str = None):
        super().__init__(systemsRecapDict)
        self.color = color
        self.title = title


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getWarningLevelEmote(systemRecap)} {self.getImportantStatusEmote(systemRecap)} | {self.getPositionEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)}"

        if systemRecap.marginWarning and systemRecap.importantState!= "war" and systemRecap.importantState!= "election":
            systemLine += f" {self.getInfluenceDiffLevelStr(systemRecap)}"

        systemLine +=  f"{self.getLastUpdateWarning(systemRecap)}"

        return systemLine

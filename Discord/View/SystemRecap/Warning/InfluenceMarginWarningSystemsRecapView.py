import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class InfluenceMarginWarningSystemsRecapView(SystemsRecapView):
    def __init__(self, systemsRecapDict: dict, warningLvl: int, isTitle: bool = False):
        super().__init__(systemsRecapDict)
        self.isTitle = isTitle

        match warningLvl:
            case 3:
                self.color = discord.Color.red()
            case 2:
                self.color = discord.Color.orange()
            case 1:
                self.color = discord.Color.yellow()

        if isTitle:
            self.title = f"{BotConfig.emotes.minorFaction.influence.down} Influence Margin Warning Level {warningLvl} {BotConfig.emotes.minorFaction.influence.down} (Inf Margin < {self.get_influence_warning_percent(warningLvl)})"

    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)}"

        if systemRecap.marginWarning and systemRecap.importantState!= "war" and systemRecap.importantState!= "election":
            systemLine += f" {self.getInfluenceDiffLevelStr(systemRecap)}"

        systemLine +=  f"{self.getLastUpdateWarning(systemRecap)}"

        return systemLine

    def get_influence_warning_percent(self, warning: str):
        if warning==1:
            return f"{round(BotConfig.bgs.leader_influence_warning.level1*100,1)}%"
        elif warning==2:
            return f"{round(BotConfig.bgs.leader_influence_warning.level2*100,1)}%"
        elif warning==3:
            return f"{round(BotConfig.bgs.leader_influence_warning.level3*100,1)}%"

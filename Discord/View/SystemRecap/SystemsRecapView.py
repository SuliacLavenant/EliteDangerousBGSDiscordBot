import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

class SystemsRecapView(discord.ui.View):
    def __init__(self, systemsRecap: dict, color: int = None, title: str = None):
        super().__init__()
        self.systemsRecap = systemsRecap
        self.color = color
        self.title = title


    def getEmbed(self):
        description=""
        i=0
        for systemRecap in self.systemsRecap.values():
            description += self.getSystemRecapOneLine(systemRecap)
            description += "\n"
            i+=1
            if i>15:
                break
        
        if self.color!=None:
            embed = discord.Embed(title=self.title, description=description, color=discord.Color(self.color))
        else:
            embed = discord.Embed(title=self.title, description=description)

        return embed


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getWarningLevelEmote(systemRecap)} {self.getImportantStatusEmote(systemRecap)} | {self.getPositionEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} **{round(systemRecap.influence*100,1)}**%"

        if systemRecap.marginWarning and systemRecap.importantState!= "war" and systemRecap.importantState!= "election":
            systemLine += f" {self.getInfluenceDiffLevelStr(systemRecap)}"

        systemLine +=  f"{self.getLastUpdateWarning(systemRecap)}"

        return systemLine


    def getSystemNameWithInaraLink(self, systemRecap: SystemMinorFactionRecap):
        return f"[**{systemRecap.system.name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(systemRecap.system.name)})"

    
    def getPositionEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.positionInSystem:
            case "leader":
                return BotConfig.positionInSystemEmotes["leader"]
            case "other":
                return BotConfig.positionInSystemEmotes["other"]


    def getImportantStatusEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.importantState:
            case None:
                return BotConfig.emotesN.minorFaction.state.none
            case "war" | "civil war":
                return BotConfig.emotesN.minorFaction.state.war
            case "election":
                return BotConfig.emotesN.minorFaction.state.election
            case "retreat":
                return BotConfig.emotesN.minorFaction.state.retreat
    

    def getNumberFactionEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.numberOfFactions<=3:
            return BotConfig.emotesN.system.numberOfMinorFaction[3]
        elif systemRecap.numberOfFactions>=7:
            return BotConfig.emotesN.system.numberOfMinorFaction[7]
        else:
            return BotConfig.emotesN.system.numberOfMinorFaction[systemRecap.numberOfFactions]
        
    def getSpecialSystemEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isOrigin:
            return BotConfig.emotesN.system.information.origin
        elif systemRecap.isArchitect:
            return BotConfig.emotesN.system.information.architect
        else:
            return BotConfig.emotesN.nothing


    def getWarningLevelEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.warning:
            case "expansion":
                return BotConfig.emotes["warningExpansion"]
            case None:
                return BotConfig.emotes["warningLevelOther"]
            case "marginLvl0":
                return BotConfig.emotes["warningLevel0"]
            case "marginLvl1":
                return BotConfig.emotes["warningLevel1"]
            case "marginLvl2":
                return BotConfig.emotes["warningLevel2"]
            case "marginLvl3":
                return BotConfig.emotes["warningLevel3"]
            case "state":
                return BotConfig.emotes["warningImportantState"]


    def getInfluenceDiffLevelStr(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isLeader:
            return f"(+{round(systemRecap.leaderInfluenceMargin*100,1)}%)"
        else:
            return f"(-{round((systemRecap.leaderInfluence-systemRecap.influence)*100,1)}%)"


    def getLastUpdateWarning(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.daysSinceLastUpdate<=1:
            return ""
        else:
            return f" | ({BotConfig.emotesN.warning}{systemRecap.daysSinceLastUpdate} days)"
        
        

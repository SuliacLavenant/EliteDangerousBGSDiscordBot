import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

class SystemsRecapView(discord.ui.View):
    color: discord.Color = ""
    title: str = ""
    systemsRecapDict: dict

    def __init__(self, systemsRecapDict: dict):
        super().__init__()
        self.systemsRecapDict = systemsRecapDict


    def getEmbed(self):
        description=""
        i=0
        for systemRecap in self.systemsRecapDict.values():
            description += self.getSystemRecapOneLine(systemRecap)
            description += "\n"
            i+=1
            if i>15:
                break
        
        if self.color!=None:
            embed = discord.Embed(title=self.title, description=description, color=self.color)
        else:
            embed = discord.Embed(title=self.title, description=description)

        return embed


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemNameWithInaraLink(systemRecap)}"

        return systemLine


    def getSystemNameWithInaraLink(self, systemRecap: SystemMinorFactionRecap):
        return f"[**{systemRecap.system.name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(systemRecap.system.name)})"

    
    def getPositionEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.positionInSystem:
            case "leader":
                return BotConfig.emotesN.minorFaction.positionInSystem.leader
            case "diplomatic":
                return BotConfig.emotesN.minorFaction.positionInSystem.diplomatic
            case "other":
                return BotConfig.emotesN.minorFaction.positionInSystem.other


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


    def getSystemGroupEmote(self, systemRecap: SystemMinorFactionRecap):
        emote = BotConfig.emotesN.nothing
        if systemRecap.systemGroup != None and systemRecap.systemGroup.emote != None:
            emote = systemRecap.systemGroup.emote
        return emote


    def getWarningLevelEmote(self, systemRecap: SystemMinorFactionRecap):
        emote = ""
        match systemRecap.warning:
            case "expansion":
                emote = BotConfig.emotes["warningExpansion"]
            case None:
                emote = BotConfig.emotes["warningLevelOther"]
            case "marginLvl0":
                emote = BotConfig.emotes["warningLevel0"]
            case "marginLvl1":
                emote = BotConfig.emotes["warningLevel1"]
            case "marginLvl2":
                emote = BotConfig.emotes["warningLevel2"]
            case "marginLvl3":
                emote = BotConfig.emotes["warningLevel3"]
            case "state":
                emote = BotConfig.emotes["warningImportantState"]
        
        #diplomatic
        if systemRecap.isDiplomatic:
            match systemRecap.diplomaticWarning:
                case "shouldBeLeader":
                    emote = BotConfig.emotes["warningLevel3"]
                case "shouldNotBeLeader":
                    emote = BotConfig.emotes["warningLevel3"]
                case "shouldtBeSecond":
                    emote = BotConfig.emotes["warningLevel3"]
                case "notLeaderGood":
                    emote = BotConfig.emotes["warningLevel0"]

        return emote

    
    def getInfluenceString(self, systemRecap: SystemMinorFactionRecap):
        influence = round(systemRecap.influence*100,1)
        return f"< **{influence}**% >"


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

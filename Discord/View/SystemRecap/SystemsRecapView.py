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
                return BotConfig.emotes.minorFaction.positionInSystem.leader
            case "diplomatic":
                return BotConfig.emotes.minorFaction.positionInSystem.diplomatic
            case "other":
                return BotConfig.emotes.minorFaction.positionInSystem.other


    def getImportantStatusEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.importantState:
            case None:
                return BotConfig.emotes.minorFaction.state.none
            case "war" | "civil war":
                return BotConfig.emotes.minorFaction.state.war
            case "election":
                return BotConfig.emotes.minorFaction.state.election
            case "retreat":
                return BotConfig.emotes.minorFaction.state.retreat


    def getNumberFactionEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.numberOfFactions<=3:
            return BotConfig.emotes.system.numberOfMinorFaction[3]
        elif systemRecap.numberOfFactions>=7:
            return BotConfig.emotes.system.numberOfMinorFaction[7]
        else:
            return BotConfig.emotes.system.numberOfMinorFaction[systemRecap.numberOfFactions]


    def getSpecialSystemEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isOrigin:
            return BotConfig.emotes.system.information.origin
        elif systemRecap.isArchitect:
            return BotConfig.emotes.system.information.architect
        else:
            return BotConfig.emotes.nothing


    def getSystemGroupEmote(self, systemRecap: SystemMinorFactionRecap):
        emote = BotConfig.emotes.nothing
        if systemRecap.systemGroup != None and systemRecap.systemGroup.emote != None:
            emote = systemRecap.systemGroup.emote
        return emote


    def getWarningLevelEmote(self, systemRecap: SystemMinorFactionRecap):
        emote = ""
        match systemRecap.warning:
            case "expansion":
                emote = BotConfig.emotes.minorFaction.state.expansion_warning
            case None:
                emote = BotConfig.emotes.nothing
            case "marginLvl0":
                emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level0
            case "marginLvl1":
                emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level1
            case "marginLvl2":
                emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level2
            case "marginLvl3":
                emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level3
            case "retreat":
                emote = BotConfig.emotes.minorFaction.state.retreat_warning
            case "important":
                emote = BotConfig.emotes.minorFaction.state.important
        
        #diplomatic #overide retreat warning, take care #even global warning
        if systemRecap.isDiplomatic:
            match systemRecap.diplomaticWarning:
                case "shouldBeLeader":
                    emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level3
                case "shouldNotBeLeader":
                    emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level3
                case "shouldtBeSecond":
                    emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level3
                case "notLeaderGood":
                    emote = BotConfig.emotes.minorFaction.influence.leader_influence_warning.level0

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
        if systemRecap.daysSinceLastUpdate<1:
            return ""
        else:
            return f" | ({BotConfig.emotes.warning}{systemRecap.daysSinceLastUpdate} days)"

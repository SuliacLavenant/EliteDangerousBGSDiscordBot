import discord
import urllib.parse

#custom
from BotConfig import BotConfig
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
            if i>20:
                break
        
        if self.color!=None:
            embed = discord.Embed(title=self.title, description=description, color=discord.Color(self.color))
        else:
            embed = discord.Embed(title=self.title, description=description)

        return embed


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = ""

        #faction name + inara link
        systemLine += f"{self.getWarningLevelEmote(systemRecap)} {self.getIsLeaderEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} **{round(systemRecap.influence*100,1)}**% {self.getInfluenceDiffLevelStr(systemRecap)}"

        return systemLine


    def getSystemRecapLines(self, systemRecap: SystemMinorFactionRecap):
        systemLine = ""

        #faction name + inara link
        systemLine += f"{self.getSystemNameWithInaraLink(systemRecap)}"
        systemLine += "\n"

        # is leader + influence + influence warning
        if systemRecap.isLeader:
            systemLine += f"{self.getIsLeaderEmote(systemRecap)} {self.getWarningLevelEmote(systemRecap)} | {round(systemRecap.influence*100,2)}% | (margin: {round(systemRecap.leaderInfluenceMargin*100,1)}%)"
        else:
            systemLine += f"{self.getIsLeaderEmote(systemRecap)} {self.warningLevelOtherEmote}"
            systemLine += f" | {round(systemRecap.influence*100,2)}% | (Leader influence: {round(systemRecap.leaderInfluence*100,1)}%)"
        systemLine += "\n"

        # can be kicked + number of factions
        if systemRecap.numberOfFactions<=3:
            systemLine += " ".ljust(5)+self.securisedEmote
        else:
            systemLine += " ".ljust(5)+self.notSecurisedEmote
        systemLine += f" ({systemRecap.numberOfFactions} factions present)"
        systemLine += "\n"

        return systemLine


    def getSystemNameWithInaraLink(self, systemRecap: SystemMinorFactionRecap):
        return f"[**{systemRecap.name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(systemRecap.name)})"

    
    def getIsLeaderEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isLeader:
            return BotConfig.emotes["leader"]
        else:
            return BotConfig.emotes["noLeader"]
    

    def getNumberFactionEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.numberOfFactions<=3:
            return BotConfig.emotes["minimumFaction"]
        elif systemRecap.numberOfFactions>=7:
            return BotConfig.emotes["maximumFaction"]
        else:
            return f":number_{systemRecap.numberOfFactions}:"
            #return self.notSecurisedEmote


    def getWarningLevelEmote(self, systemRecap: SystemMinorFactionRecap):
        # important states
        match systemRecap.conflictState:
            case "war" | "civil war":
                return BotConfig.emotes["war"]
            case "election":
                return BotConfig.emotes["election"]

        if systemRecap.retreatWarning:
            return BotConfig.emotes["retreat"]
        

        if systemRecap.expansionWarning:
            return BotConfig.emotes["warningExpansion"]

        if systemRecap.influenceWarningLevel == 3:
            return BotConfig.emotes["warningLevel3"]
        elif systemRecap.influenceWarningLevel == 2:
            return BotConfig.emotes["warningLevel2"]
        elif systemRecap.influenceWarningLevel == 1:
            return BotConfig.emotes["warningLevel1"]
        elif systemRecap.influenceWarningLevel == 0:
            return BotConfig.emotes["warningLevel0"]
        else:
            return BotConfig.emotes["warningLevelOther"]

    def getInfluenceDiffLevelStr(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isLeader:
            return f"(+{round(systemRecap.leaderInfluenceMargin*100,1)}%)"
        else:
            return f"(-{round((systemRecap.leaderInfluence-systemRecap.influence)*100,1)}%)"

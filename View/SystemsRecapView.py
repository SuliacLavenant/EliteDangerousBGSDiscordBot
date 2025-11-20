import discord
import urllib.parse

#custom
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

class SystemsRecapView(discord.ui.View):
    leaderEmote: str = ":crown:"
    noLeaderEmote: str = ":bust_in_silhouette:"
    inRetreatEmote: str = ":skull_crossbones:"

    maximumFactionEmote: str = ":lock:"
    minimumFactionEmote: str = ":shield:"


    warningLevelOtherEmote: str = ":white_circle:"
    warningLevel0Emote: str = ":green_circle:"
    warningLevel1Emote: str = ":yellow_circle:"
    warningLevel2Emote: str = ":orange_circle:"
    warningLevel3Emote: str = ":red_circle:"


    def __init__(self, systemsRecap: dict, title: str = None):
        super().__init__()
        self.systemsRecap = systemsRecap
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
        print(len(description))
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
            return self.leaderEmote
        elif systemRecap.retreatWarning:
            return self.inRetreatEmote
        else:
            return self.noLeaderEmote
    

    def getNumberFactionEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.numberOfFactions<=3:
            return self.minimumFactionEmote
        elif systemRecap.numberOfFactions>=7:
            return self.maximumFactionEmote
        else:
            return f":number_{systemRecap.numberOfFactions}:"
            #return self.notSecurisedEmote


    def getWarningLevelEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.influenceWarningLevel == 3 or systemRecap.retreatWarning:
            return self.warningLevel3Emote
        elif systemRecap.influenceWarningLevel == 2:
            return self.warningLevel2Emote
        elif systemRecap.influenceWarningLevel == 1:
            return self.warningLevel1Emote
        if systemRecap.influenceWarningLevel == 0:
            return self.warningLevel0Emote
        else:
            return self.warningLevelOtherEmote

    def getInfluenceDiffLevelStr(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isLeader:
            return f"(+{round(systemRecap.leaderInfluenceMargin*100,1)}%)"
        else:
            return f"(-{round((systemRecap.leaderInfluence-systemRecap.influence)*100,1)}%)"

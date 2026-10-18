import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataClass.GuildSettings import GuildSettings
# from DataClass.Squadron import Squadron
# from DataStorageManager import DataStorageManager
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

class SystemsRecapView(discord.ui.View):
    color: discord.Color = ""
    guild_settings: GuildSettings
    systemsRecapDict: dict
    title: str = ""

    def __init__(self, guild_settings: GuildSettings, systemsRecapDict: dict):
        super().__init__()
        self.guild_settings = guild_settings
        self.systemsRecapDict = systemsRecapDict


    def get_embed(self):
        description=""
        i=0
        for systemRecap in self.systemsRecapDict.values():
            description += self.get_system_recap_one_line(systemRecap)
            description += "\n"
            i+=1
            if i>15:
                break
        
        if self.color!=None:
            embed = discord.Embed(title=self.title, description=description, color=self.color)
        else:
            embed = discord.Embed(title=self.title, description=description)

        return embed


    def get_system_recap_one_line(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemNameWithInaraLink(systemRecap)}"

        return systemLine


    def getSystemNameWithInaraLink(self, systemRecap: SystemMinorFactionRecap):
        return f"[**{systemRecap.system.name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(systemRecap.system.name)})"

    
    def getPositionEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.position_in_system:
            case "leader":
                return BotConfig.emotes.minorFaction.positionInSystem.leader
            case "diplomatic":
                return BotConfig.emotes.minorFaction.positionInSystem.diplomatic
            case "other":
                return BotConfig.emotes.minorFaction.positionInSystem.other
            case None:
                return BotConfig.emotes.minorFaction.positionInSystem.none


    def getImportantStatusEmote(self, systemRecap: SystemMinorFactionRecap):
        match systemRecap.important_state:
            case None:
                return BotConfig.emotes.minorFaction.state.none
            case "war" | "civil war":
                return BotConfig.emotes.minorFaction.state.war
            case "election":
                return BotConfig.emotes.minorFaction.state.election
            case "retreat":
                return BotConfig.emotes.minorFaction.state.retreat


    def getNumberFactionEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.number_of_factions<=3:
            return BotConfig.emotes.system.numberOfMinorFaction[3]
        elif systemRecap.number_of_factions>=7:
            return BotConfig.emotes.system.numberOfMinorFaction[7]
        else:
            return BotConfig.emotes.system.numberOfMinorFaction[systemRecap.number_of_factions]


    def getSpecialSystemEmote(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.isOrigin:
            return BotConfig.emotes.system.information.origin
        if systemRecap.system.is_architected:
            if self.guild_settings.squadron_id != None:
                squadron: Squadron = DataStorageManager.get_squadron_by_id(self.guild_settings.guild_id, self.guild_settings.squadron_id)
                if squadron.get_player_position_in_squadron(systemRecap.system.architect_id) != None:
                    return BotConfig.emotes.system.information.architect

        return BotConfig.emotes.nothing


    #TODO fix
    def get_system_group_emote(self, systemRecap: SystemMinorFactionRecap):
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
        if systemRecap.is_diplomatic:
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
        if systemRecap.is_leader:
            return f"(+{round(systemRecap.leader_influence_margin*100,1)}%)"
        else:
            return f"(-{round((systemRecap.leader_influence-systemRecap.influence)*100,1)}%)"


    def getLastUpdateWarning(self, systemRecap: SystemMinorFactionRecap):
        if systemRecap.days_since_last_update is None or systemRecap.days_since_last_update<1:
            return ""
        else:
            return f" | ({BotConfig.emotes.warning}{systemRecap.days_since_last_update} days)"


    def get_have_mission_string(self, systemRecap: SystemMinorFactionRecap):
        if len(systemRecap.system.mission_ids)>=1:
            return f" | {BotConfig.emotes.mission.mission}"
        else:
            return ""

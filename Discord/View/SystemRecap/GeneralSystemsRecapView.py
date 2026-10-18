import discord

from DataClass.GuildSettings import GuildSettings
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap
from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class GeneralSystemsRecapView(SystemsRecapView):
    def __init__(self, guild_settings: GuildSettings, systemsRecapDict: dict, color: discord.Color = None, title: str = None):
        super().__init__(guild_settings, systemsRecapDict)
        self.color = color
        self.title = title


    def get_system_recap_one_line(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getWarningLevelEmote(systemRecap)} {self.getImportantStatusEmote(systemRecap)} | {self.getPositionEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)}"

        if systemRecap.margin_warning and systemRecap.important_state!= "war" and systemRecap.important_state!= "election":
            systemLine += f" {self.getInfluenceDiffLevelStr(systemRecap)}"

        #systemLine +=  f"{self.get_have_mission_string(systemRecap)}"
        systemLine +=  f"{self.getLastUpdateWarning(systemRecap)}"

        return systemLine

import discord

from DataClass.GuildSettings import GuildSettings
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class InfluenceMarginWarningSystemsRecapView(SystemsRecapView):
    def __init__(self, guild_settings: GuildSettings, systemsRecapDict: dict, warningLvl: int, isTitle: bool = False):
        super().__init__(guild_settings, systemsRecapDict)
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

    def get_system_recap_one_line(self, system_recap: SystemMinorFactionRecap):
        systemLine = f"{self.get_system_group_emote(system_recap)} | {self.getNumberFactionEmote(system_recap)} {self.getSpecialSystemEmote(system_recap)} | {self.getSystemNameWithInaraLink(system_recap)} | {self.getInfluenceString(system_recap)}"

        if system_recap.margin_warning and system_recap.important_state != "war" and system_recap.important_state != "election":
            systemLine += f" {self.getInfluenceDiffLevelStr(system_recap)}"

        systemLine +=  f"{self.getLastUpdateWarning(system_recap)}"

        return systemLine

    def get_influence_warning_percent(self, warning: str):
        if warning==1:
            return f"{round(BotConfig.bgs.leader_influence_warning.level1*100,1)}%"
        elif warning==2:
            return f"{round(BotConfig.bgs.leader_influence_warning.level2*100,1)}%"
        elif warning==3:
            return f"{round(BotConfig.bgs.leader_influence_warning.level3*100,1)}%"

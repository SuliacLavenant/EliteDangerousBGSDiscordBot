import discord

from DataClass.GuildSettings import GuildSettings
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class ConflictSystemsRecapView(SystemsRecapView):
    def __init__(self, guild_settings: GuildSettings, systemsRecapDict: dict, isTitle: bool = False):
        super().__init__(guild_settings, systemsRecapDict)
        self.isTitle = isTitle
        self.color = discord.Color.red()

        if isTitle:
            self.title = f"{BotConfig.emotes.minorFaction.state.war}{BotConfig.emotes.minorFaction.state.election} Conflicts (War and Election) {BotConfig.emotes.minorFaction.state.election}{BotConfig.emotes.minorFaction.state.war}"


    def get_system_recap_one_line(self, system_recap: SystemMinorFactionRecap):
        systemLine = f"{self.get_system_group_emote(system_recap)} | {self.getImportantStatusEmote(system_recap)} | {self.getPositionEmote(system_recap)} {self.getNumberFactionEmote(system_recap)} {self.getSpecialSystemEmote(system_recap)} | {self.getSystemNameWithInaraLink(system_recap)} {self.getLastUpdateWarning(system_recap)}"

        return systemLine

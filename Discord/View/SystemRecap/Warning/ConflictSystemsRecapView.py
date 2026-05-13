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


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getImportantStatusEmote(systemRecap)} | {self.getPositionEmote(systemRecap)} {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

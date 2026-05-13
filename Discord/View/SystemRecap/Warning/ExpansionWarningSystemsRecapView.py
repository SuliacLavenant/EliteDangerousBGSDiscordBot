import discord

from DataClass.GuildSettings import GuildSettings
from BotConfig.BotConfig import BotConfig
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView

class ExpansionWarningSystemsRecapView(SystemsRecapView):
    def __init__(self, guild_settings: GuildSettings, systemsRecapDict: dict, isTitle: bool = False):
        super().__init__(guild_settings, systemsRecapDict)
        self.isTitle = isTitle
        self.color = discord.Color.blue()

        if isTitle:
            self.title = f"{BotConfig.emotes.minorFaction.state.expansion} Expansion Warning {BotConfig.emotes.minorFaction.state.expansion}"


    def getSystemRecapOneLine(self, systemRecap: SystemMinorFactionRecap):
        systemLine = f"{self.getSystemGroupEmote(systemRecap)} | {self.getNumberFactionEmote(systemRecap)} {self.getSpecialSystemEmote(systemRecap)} | {self.getSystemNameWithInaraLink(systemRecap)} | {self.getInfluenceString(systemRecap)} {self.getLastUpdateWarning(systemRecap)}"

        return systemLine

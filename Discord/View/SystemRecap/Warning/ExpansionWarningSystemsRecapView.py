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


    def get_system_recap_one_line(self, system_recap: SystemMinorFactionRecap):
        systemLine = f"{self.get_system_group_emote(system_recap)} | {self.getNumberFactionEmote(system_recap)} {self.getSpecialSystemEmote(system_recap)} | {self.getSystemNameWithInaraLink(system_recap)} | {self.getInfluenceString(system_recap)} {self.getLastUpdateWarning(system_recap)}"

        return systemLine

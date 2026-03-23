import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataClass.MinorFaction import MinorFaction
from DataClass.System import System
from DataStorageManager import DataStorageManager
from PermissionManager.PermissionManager import PermissionManager


class MinorFactionSharedSystemsView(discord.ui.View):
    systems: list
    minor_faction: MinorFaction
    guild_minor_faction: MinorFaction

    def __init__(self, systems: list, minor_faction: MinorFaction, guild_minor_faction: MinorFaction):
        super().__init__()
        self.systems = systems
        self.minor_faction = minor_faction
        self.guild_minor_faction = guild_minor_faction


    def getEmbed(self):
        title = f"Shared Systems"
        embed = discord.Embed(title=title)
        for system in self.systems:
            emote = self.get_minor_faction_emote(system,self.minor_faction.name)
            minor_faction_line = f"{emote} **{self.minor_faction.name}** {emote} - <**{round(system.minor_factions_influence[self.minor_faction.name.lower()]*100,1)}%**>\n"

            emote = self.get_minor_faction_emote(system,self.guild_minor_faction.name)
            guild_minor_faction_line = f"{emote} **{self.guild_minor_faction.name}** {emote} - <**{round(system.minor_factions_influence[self.guild_minor_faction.name.lower()]*100,1)}%**> {BotConfig.emotesN.pin}\n"

            value = ""
            if system.controlling_faction_name.lower() == self.minor_faction.name.lower():
                value = minor_faction_line + guild_minor_faction_line
            elif system.controlling_faction_name.lower() == self.guild_minor_faction.name.lower():
                value = guild_minor_faction_line + minor_faction_line
            else:
                emote = self.get_minor_faction_emote(system,system.controlling_faction_name)
                value = f"{emote} **{system.controlling_faction_name}** {emote} - <**{round(system.minor_factions_influence[system.controlling_faction_name.lower()]*100,1)}%**>\n"
                if system.minor_factions_influence[self.minor_faction.name.lower()] > system.minor_factions_influence[self.guild_minor_faction.name.lower()]:
                    value += minor_faction_line
                    value += guild_minor_faction_line
                else:
                    value += guild_minor_faction_line
                    value += minor_faction_line

            embed.add_field(name=system.name, value=value, inline=False)

        return embed


    def get_minor_faction_emote(self, system: System, minor_faction_name: str):
        if system.controlling_faction_name.lower() == minor_faction_name.lower():
            return BotConfig.emotesN.minorFaction.positionInSystem.leader
        else:
            return BotConfig.emotesN.minorFaction.positionInSystem.other

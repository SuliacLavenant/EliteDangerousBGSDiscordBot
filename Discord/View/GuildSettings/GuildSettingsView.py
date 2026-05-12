import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from DataClass.Squadron import Squadron
from PermissionManager.PermissionManager import PermissionManager

class GuildSettingsView(discord.ui.View):
    guild_settings: GuildSettings

    def __init__(self, guild_settings: GuildSettings):
        super().__init__()
        self.guild_settings = guild_settings


    def getEmbed(self):
        title: str = f"Guild Settings"
        description: str = ""
        if self.guild_settings.minor_faction_name != None:
            description += f"**Minor Faction:** {self.guild_settings.minor_faction_name}\n"
        else:
            description += f"**Minor Faction:** None\n"
        if self.guild_settings.squadron_id != None:
            squadron: Squadron = DataStorageManager.get_squadron_by_id(self.guild_settings.guild_id, self.guild_settings.squadron_id)
            description += f"**Squadron:** {squadron.name}\n"
        else:
            description += f"**Squadron:** None\n"

        embed = discord.Embed(title=title, description=description)

        #Channels
        channels_description = ""
        channels_description += f"All Systems Recap Channel: "
        if self.guild_settings.bgs_system_recap_channel_id != None:
            channels_description += f"<#{self.guild_settings.bgs_system_recap_channel_id}>\n"
        else:
            channels_description += f"Not set\n"

        channels_description += f"Warning Recap Channel: "
        if self.guild_settings.bgs_warning_recap_channel_id != None:
            channels_description += f"<#{self.guild_settings.bgs_warning_recap_channel_id}>\n"
        else:
            channels_description += f"**Not set**\n"

        channels_description += f"Change Log Channel: "
        if self.guild_settings.bgs_change_log_channel_id != None:
            channels_description += f"<#{self.guild_settings.bgs_change_log_channel_id}>\n"
        else:
            channels_description += f"**Not set**\n"

        channels_description += f"Mission Recap Channel: "
        if self.guild_settings.mission_recap_channel_id != None:
            channels_description += f"<#{self.guild_settings.mission_recap_channel_id}>\n"
        else:
            channels_description += f"**Not set**\n"

        channels_description += f"Trusted Channels: "
        for channel_id in self.guild_settings.trusted_channel_ids:
            channels_description += f"<#{channel_id}>,"
        channels_description += f"\n"

        embed.add_field(name="Channels", value=channels_description, inline=False)

        return embed

import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from PermissionManager.PermissionManager import PermissionManager

class GuildSettingsView(discord.ui.View):
    def __init__(self, guild_settings: GuildSettings):
        super().__init__()
        self.guild_settings = guild_settings


    def getEmbed(self):
        title = f"Guild Settings"
        description = ""
        description += f"**Minor Faction:** {self.guild_settings.minor_faction_name}"

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

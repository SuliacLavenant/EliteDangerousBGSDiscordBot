import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from Discord.View.GuildSettings.GuildSettingsView import GuildSettingsView
from Discord.View.GuildSettings.ChannelGuildSettingsView import ChannelGuildSettingsView
from PermissionManager.PermissionManager import PermissionManager

class DefaultGuildSettingsView(GuildSettingsView):
    def __init__(self, guild_settings: GuildSettings):
        super().__init__(guild_settings)


    @discord.ui.button(label="Manage Channels", style=discord.ButtonStyle.secondary, row=1)
    async def manage_channels(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            channel_guild_settings_view = ChannelGuildSettingsView(guild_settings,interaction.channel_id)
            await interaction.response.edit_message(embed=channel_guild_settings_view.getEmbed(),view=channel_guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)

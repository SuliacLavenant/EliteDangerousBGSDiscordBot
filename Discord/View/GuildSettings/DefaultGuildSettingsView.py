import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from DataClass.Squadron import Squadron
from Discord.Modal.GuildSettings.SetSquadronModal import SetSquadronModal
from Discord.View.GuildSettings.GuildSettingsView import GuildSettingsView
from Discord.View.GuildSettings.ChannelGuildSettingsView import ChannelGuildSettingsView
from PermissionManager.PermissionManager import PermissionManager

class DefaultGuildSettingsView(GuildSettingsView):
    def __init__(self, guild_settings: GuildSettings):
        super().__init__(guild_settings)


    @discord.ui.button(label="Set Squadron", style=discord.ButtonStyle.secondary, row=1)
    async def set_squadron(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_squadron(interaction.user.id):
            squadrons: list[Squadron] = DataStorageManager.get_squadrons(interaction.guild_id)
            set_squadron_modal: SetSquadronModal = SetSquadronModal(squadrons)
            await interaction.response.send_modal(set_squadron_modal)
            await set_squadron_modal.wait()

            if set_squadron_modal.squadron_id != None:
                guild_settings: GuildSettings = DataStorageManager.get_guild_settings(interaction.guild_id)
                guild_settings.squadron_id = set_squadron_modal.squadron_id
                DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings: GuildSettings = DataStorageManager.get_guild_settings(interaction.guild_id)
            deffault_guild_settings_view = DefaultGuildSettingsView(guild_settings)
            await interaction.message.edit(embed=deffault_guild_settings_view.getEmbed(), view=deffault_guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Manage Channels", style=discord.ButtonStyle.secondary, row=1)
    async def manage_channels(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings: GuildSettings = DataStorageManager.get_guild_settings(interaction.guild_id)
            channel_guild_settings_view = ChannelGuildSettingsView(guild_settings,interaction.channel_id)
            await interaction.response.edit_message(embed=channel_guild_settings_view.getEmbed(),view=channel_guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)

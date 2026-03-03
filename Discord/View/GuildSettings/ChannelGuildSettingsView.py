import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from Discord.View.GuildSettings.GuildSettingsView import GuildSettingsView
from PermissionManager.PermissionManager import PermissionManager

class ChannelGuildSettingsView(GuildSettingsView):
    def __init__(self, guild_settings: GuildSettings, current_channel_id: int):
        super().__init__(guild_settings)

        if self.guild_settings.bgs_system_recap_channel_id == None:
            self.unset_system_recap_channel.disabled = True
        elif self.guild_settings.bgs_system_recap_channel_id == current_channel_id:
            self.set_system_recap_channel.disabled = True

        if self.guild_settings.bgs_warning_recap_channel_id == None:
            self.unset_warning_recap_channel.disabled = True
        elif self.guild_settings.bgs_warning_recap_channel_id == current_channel_id:
            self.set_warning_recap_channel.disabled = True

        if self.guild_settings.bgs_change_log_channel_id == None:
            self.unset_change_log_channel.disabled = True
        elif self.guild_settings.bgs_change_log_channel_id == current_channel_id:
            self.set_change_log_channel.disabled = True

        if self.guild_settings.mission_recap_channel_id == None:
            self.unset_mission_recap_channel.disabled = True
        elif self.guild_settings.mission_recap_channel_id == current_channel_id:
            self.set_mission_recap_channel.disabled = True

        if current_channel_id in self.guild_settings.trusted_channel_ids:
            self.add_as_trusted_channel.disabled = True
        else:
            self.remove_from_trusted_channel.disabled = True


    @discord.ui.button(label="Set System Recap Channel", style=discord.ButtonStyle.primary, row=0)
    async def set_system_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_system_recap_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Unset System Recap Channel", style=discord.ButtonStyle.danger, row=0)
    async def unset_system_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_system_recap_channel_id = None
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Warning Recap Channel", style=discord.ButtonStyle.primary, row=1)
    async def set_warning_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_warning_recap_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Unset Warning Recap Channel", style=discord.ButtonStyle.danger, row=1)
    async def unset_warning_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_warning_recap_channel_id = None
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Change Log Channel", style=discord.ButtonStyle.primary, row=2)
    async def set_change_log_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_change_log_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Unset Change Log Channel", style=discord.ButtonStyle.danger, row=2)
    async def unset_change_log_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_change_log_channel_id = None
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Mission Recap Channel", style=discord.ButtonStyle.primary, row=3)
    async def set_mission_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.mission_recap_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Unset Mission Recap Channel", style=discord.ButtonStyle.danger, row=3)
    async def unset_mission_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.mission_recap_channel_id = None
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Add As trusted Channel", style=discord.ButtonStyle.primary, row=4)
    async def add_as_trusted_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.add_trusted_channel(interaction.channel_id)
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Remove from trusted Channel", style=discord.ButtonStyle.danger, row=4)
    async def remove_from_trusted_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.remove_trusted_channel(interaction.channel_id)
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.edit_message(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)

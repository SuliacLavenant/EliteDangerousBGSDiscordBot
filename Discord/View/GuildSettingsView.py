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


    @discord.ui.button(label="Set System Recap Channel", style=discord.ButtonStyle.secondary, row=1)
    async def set_system_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            #update settings
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_system_recap_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.send_message(f"BGS System Recap Channel <#{guild_settings.bgs_system_recap_channel_id}> succesfully set!", ephemeral=True)
            await interaction.message.edit(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Warning Recap Channel", style=discord.ButtonStyle.secondary, row=1)
    async def set_warning_recap_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            #update settings
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_warning_recap_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.send_message(f"BGS Warning Recap Channel <#{guild_settings.bgs_warning_recap_channel_id}> succesfully set!", ephemeral=True)
            await interaction.message.edit(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Change Log Channel", style=discord.ButtonStyle.secondary, row=1)
    async def set_change_log_channel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            #update settings
            guild_settings = DataStorageManager.get_guild_settings(interaction.guild_id)
            guild_settings.bgs_change_log_channel_id = interaction.channel_id
            DataStorageManager.store_guild_settings(interaction.guild_id, guild_settings)

            guild_settings_view = GuildSettingsView(guild_settings)
            await interaction.response.send_message(f"BGS Warning Recap Channel <#{guild_settings.bgs_change_log_channel_id}> succesfully set!", ephemeral=True)
            await interaction.message.edit(embed=guild_settings_view.getEmbed(),view=guild_settings_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


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
        embed.add_field(name="Channels", value=channels_description, inline=False)

        return embed

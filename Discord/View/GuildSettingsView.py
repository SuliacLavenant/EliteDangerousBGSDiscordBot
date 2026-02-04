import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataStorageManager import DataStorageManager
from DataClass.GuildSettings import GuildSettings
from PermissionManager.PermissionManager import PermissionManager

class GuildSettingsView(discord.ui.View):
    def __init__(self, guildSettings: GuildSettings):
        super().__init__()
        self.guildSettings = guildSettings


    @discord.ui.button(label="Set System Recap Channel", style=discord.ButtonStyle.secondary, row=1)
    async def setSystemRecapChannel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            #update settings
            guildSettings = DataStorageManager.getGuildSettings(interaction.guild_id)
            guildSettings.bgsSystemRecapChannelID = interaction.channel_id
            DataStorageManager.storeGuildSettings(interaction.guild_id, guildSettings)

            guildSettingsView = GuildSettingsView(guildSettings)
            await interaction.response.send_message(f"BGS System Recap Channel <#{guildSettings.bgsSystemRecapChannelID}> succesfully set!", ephemeral=True)
            await interaction.message.edit(embed=guildSettingsView.getEmbed(),view=guildSettingsView)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Warning Recap Channel", style=discord.ButtonStyle.secondary, row=1)
    async def setWarningRecapChannel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.guild_settings_permissions.set_channel(interaction.user.id):
            #update settings
            guildSettings = DataStorageManager.getGuildSettings(interaction.guild_id)
            guildSettings.bgsWarningRecapChannelID = interaction.channel_id
            DataStorageManager.storeGuildSettings(interaction.guild_id, guildSettings)

            guildSettingsView = GuildSettingsView(guildSettings)
            await interaction.response.send_message(f"BGS Warning Recap Channel <#{guildSettings.bgsWarningRecapChannelID}> succesfully set!", ephemeral=True)
            await interaction.message.edit(embed=guildSettingsView.getEmbed(),view=guildSettingsView)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def getEmbed(self):
        title = f"Guild Settings"
        description = ""
        description += f"**Minor Faction:** {self.guildSettings.minorFactionName}"

        embed = discord.Embed(title=title, description=description)

        #Channels
        channelsDescription = ""
        channelsDescription += f"**All Systems Recap Channel:** "
        if self.guildSettings.bgsSystemRecapChannelID != None:
            channelsDescription += f"<#{self.guildSettings.bgsSystemRecapChannelID}>\n"
        else:
            channelsDescription += f"Not set\n"
        channelsDescription += f"Warning Recap Channel: "
        if self.guildSettings.bgsWarningRecapChannelID != None:
            channelsDescription += f"<#{self.guildSettings.bgsWarningRecapChannelID}>\n"
        else:
            channelsDescription += f"Not set\n"
        embed.add_field(name="Channels", value=channelsDescription, inline=False)

        return embed

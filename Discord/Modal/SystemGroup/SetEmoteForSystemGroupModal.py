import discord

from DataClass.SystemGroup import SystemGroup
from DataStorageManager import DataStorageManager

class SetEmoteForSystemGroupModal(discord.ui.Modal):
    def __init__(self, systemGroup: SystemGroup):
        super().__init__(title="Set Emote for System Group")
        self.systemGroup = systemGroup

        self.emote = discord.ui.InputText(label="Emote")
        self.add_item(self.emote)

    async def callback(self, interaction: discord.Interaction):
        self.systemGroup.emote = self.emote.value
        DataStorageManager.storeSystemGroup(interaction.guild_id, self.systemGroup)
        await interaction.response.send_message(f"Emote: {self.emote.value}", ephemeral=True)

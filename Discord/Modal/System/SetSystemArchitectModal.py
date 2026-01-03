import discord

from DataManager import DataManager

class SetSystemArchitectModal(discord.ui.Modal):
    def __init__(self, system):
        super().__init__(title="Set System Architect")
        self.system = system

        self.architectName = discord.ui.InputText(label="Architect Name")
        self.add_item(self.architectName)

    async def callback(self, interaction: discord.Interaction):
        if DataManager.setSystemArchitect(interaction.guild_id,self.system.name,self.architectName.value.lower()):
            await interaction.response.send_message(f"Architect name: {self.architectName.value} successfully set", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: Issue while seting Architect name: {self.architectName.value}", ephemeral=True)
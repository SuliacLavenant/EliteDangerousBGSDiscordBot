import discord

from DataStorageManager import DataStorageManager

class CreateSystemGroupModal(discord.ui.Modal):
    new_system_group: bool = False

    def __init__(self):
        super().__init__(title="Create System Group")

        self.system_group_name_input = discord.ui.InputText(label="System Group Name")
        self.add_item(self.system_group_name_input)

    async def callback(self, interaction: discord.Interaction):
        system_group_name = str(self.system_group_name_input.value)

        if system_group_name not in DataStorageManager.getSystemGroupNames(interaction.guild_id):
            self.new_system_group = True
            await interaction.response.send_message(f"System Group name: \"{self.system_group_name_input.value}\"", ephemeral=True)
        else:
            await interaction.response.send_message(f"System Group \"{self.system_group_name_input.value}\" already exist!", ephemeral=True)

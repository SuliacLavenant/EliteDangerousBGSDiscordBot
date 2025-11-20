import discord

class CreateSystemGroupModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create System Group")

        self.systemGroupName = discord.ui.InputText(label="Group Name")
        self.add_item(self.systemGroupName)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"System Group name: {self.systemGroupName.value}", ephemeral=True)
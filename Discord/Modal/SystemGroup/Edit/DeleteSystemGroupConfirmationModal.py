import discord

class DeleteSystemGroupConfirmationModal(discord.ui.Modal):
    def __init__(self, systemGroupName: str):
        super().__init__(title=f"Delete System Group: {systemGroupName}")
        self.systemGroupName = systemGroupName

        self.systemGroupNameInput = discord.ui.InputText(
            label="Enter System Group Name to confirm",
            placeholder=self.systemGroupName,
            required=True
            )
        self.add_item(self.systemGroupNameInput)

    async def callback(self, interaction: discord.Interaction):
        textInput = self.systemGroupNameInput.value

        if textInput == self.systemGroupName:
            await interaction.response.send_message("Confirmed the Deletion.",ephemeral=True)
        else:
            await interaction.response.send_message("Cases do not match, deletion cancelled.",ephemeral=True)

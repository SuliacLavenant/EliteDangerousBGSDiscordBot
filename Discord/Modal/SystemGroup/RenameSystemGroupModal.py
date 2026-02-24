import discord

class RenameSystemGroupModal(discord.ui.DesignerModal):
    def __init__(self):
        super().__init__(title="Rename System Group")

        self.name_input = discord.ui.Label(label="Name:").set_input_text()
        self.add_item(self.name_input)


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

import discord

class CreateSystemGroupModal(discord.ui.DesignerModal):
    def __init__(self):
        super().__init__(title="Create System Group")

        self.system_group_name_input = discord.ui.Label(label="Name:").set_input_text()
        self.add_item(self.system_group_name_input)


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.system_group_name = str(self.system_group_name_input.item.value)

import discord

from DataClass.Player import Player

class AddOtherNamePlayerModal(discord.ui.Modal):
    other_name: str
    player: Player

    def __init__(self, player: Player):
        super().__init__(title="Add other name for Player")
        self.player = player

        self.other_name_input = discord.ui.InputText(label="Other Name:")
        self.add_item(self.other_name_input)


    async def callback(self, interaction: discord.Interaction):
        self.other_name = self.other_name_input.value
        await interaction.response.defer()

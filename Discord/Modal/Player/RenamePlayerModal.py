import discord

from DataClass.Player import Player
from DataManager import DataManager

class RenamePlayerModal(discord.ui.Modal):
    player_name: str
    player: Player

    def __init__(self, player: Player):
        super().__init__(title="Change Player Name")
        self.player = player

        self.player_name_input = discord.ui.InputText(label="Player Name:")
        self.player_name_input.value = player.name
        self.add_item(self.player_name_input)


    async def callback(self, interaction: discord.Interaction):
        self.player_name = self.player_name_input.value
        await interaction.response.defer()

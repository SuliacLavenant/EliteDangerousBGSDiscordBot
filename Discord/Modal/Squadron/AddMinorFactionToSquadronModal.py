import discord

from DataClass.Squadron import Squadron
from DataManager import DataManager

class AddMinorFactionToSquadronModal(discord.ui.Modal):
    minor_faction_name: str
    squadron: Squadron

    def __init__(self, squadron: Squadron):
        super().__init__(title="Add A Minor Faction To Squadron")
        self.squadron = squadron

        self.minor_faction_name_input = discord.ui.InputText(label="Minor Faction Name To Add:")
        self.add_item(self.minor_faction_name_input)


    async def callback(self, interaction: discord.Interaction):
        self.minor_faction_name = self.minor_faction_name_input.value
        await interaction.response.defer()

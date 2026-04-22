import discord

from DataClass.Squadron import Squadron
from DataManager import DataManager

class ChangeSquadronTagModal(discord.ui.Modal):
    squadron_tag: str
    squadron: Squadron

    def __init__(self, squadron: Squadron):
        super().__init__(title="Change Squadron Tag")
        self.squadron = squadron

        self.squadron_tag_input = discord.ui.InputText(label="Squadron Tag:")
        self.squadron_tag_input.value = squadron.tag
        self.add_item(self.squadron_tag_input)


    async def callback(self, interaction: discord.Interaction):
        self.squadron_tag = self.squadron_tag_input.value
        await interaction.response.defer()

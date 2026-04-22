import discord

from DataClass.Squadron import Squadron
from DataManager import DataManager

class RemoveMinorFactionFromSquadronModal(discord.ui.DesignerModal):
    minor_faction_name: str
    squadron: Squadron

    def __init__(self, squadron: Squadron):
        super().__init__(title="Remove A Minor Faction From Squadron")
        self.squadron = squadron

        options = []
        for minor_faction_name in self.squadron.minor_faction_names:
            options.append(discord.SelectOption(label=minor_faction_name, value=minor_faction_name))
        self.minor_faction_name_select = discord.ui.Label(label="Minor Faction Name To Remove:").set_select(
            options=options,
            min_values=1,
            max_values=1,
            default_values=None,
            required=True
        )
        self.add_item(self.minor_faction_name_select)


    async def callback(self, interaction: discord.Interaction):
        self.minor_faction_name = self.minor_faction_name_select.item.values[0]
        await interaction.response.defer()

import discord

class SetMinorFactionModal(discord.ui.DesignerModal):
    def __init__(self):
        super().__init__(title="Set Minor Faction Modal")

        self.minor_faction_name_input = discord.ui.Label(label="Minor Faction Name:").set_input_text()
        self.add_item(self.minor_faction_name_input)


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.minor_faction_name = str(self.minor_faction_name_input.item.value)

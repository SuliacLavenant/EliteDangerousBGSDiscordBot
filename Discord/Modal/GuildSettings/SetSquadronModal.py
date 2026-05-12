import discord

from DataClass.Squadron import Squadron

class SetSquadronModal(discord.ui.DesignerModal):
    squadrons: list[Squadron]
    squadron_select: discord.ui.Label
    squadron_id: int = None

    def __init__(self, squadrons: list[Squadron]):
        super().__init__(title=f"Select Squadron")
        self.squadrons = squadrons

        options = []
        for squadron in self.squadrons:
            options.append(discord.SelectOption(label=squadron.name, value=str(squadron.id)))
        self.squadron_select = discord.ui.Label(label="Squadron:").set_select(
            options=options,
            min_values=1,
            max_values=1,
            default_values=None,
            required=True
        )
        self.add_item(self.squadron_select)


    async def callback(self, interaction: discord.Interaction):
        self.squadron_id = int(self.squadron_select.item.values[0])

        await interaction.response.defer()

import discord

from DataClass.System import System

class CreateRetreatMinorFactionFromSystemMissionModal(discord.ui.DesignerModal):
    minor_faction: str
    system: System

    def __init__(self, system: System):
        super().__init__(title=f"Create Retreat Mission On System")
        self.system = system

        minor_faction_names = self.system.get_minor_faction_names()

        options = []
        for minor_faction_name in minor_faction_names:
            options.append(discord.SelectOption(label=minor_faction_name, value=minor_faction_name))
        
        self.minor_faction_select = discord.ui.Label(label="Minor Faction To Retreat:").set_select(
            options=options,
            min_values=1,
            max_values=1,
            default_values=None,
            required=True
        )
        self.add_item(self.minor_faction_select)


    async def callback(self, interaction: discord.Interaction):
        self.minor_faction = self.minor_faction_select.item.values[0]
        await interaction.response.defer()

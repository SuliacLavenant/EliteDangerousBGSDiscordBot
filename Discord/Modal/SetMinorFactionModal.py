import discord

class SetMinorFactionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Set Minor Faction")

        self.minorFactionName = discord.ui.InputText(label="Minor Faction Name")
        self.add_item(self.minorFactionName)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Minor Faction name: {self.minorFactionName.value}", ephemeral=True)
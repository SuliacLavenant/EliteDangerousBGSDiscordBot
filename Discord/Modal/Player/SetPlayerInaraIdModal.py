import discord


class SetPlayerInaraIdModal(discord.ui.Modal):
    inara_id: int = None


    def __init__(self):
        super().__init__(title="Set Player Inara Id")

        self.inara_id_input = discord.ui.InputText(label="Inara Id:")
        self.add_item(self.inara_id_input)


    async def callback(self, interaction: discord.Interaction):
        if self.inara_id_input.value.isdigit():
            self.inara_id = int(self.inara_id_input.value)
        await interaction.response.defer()

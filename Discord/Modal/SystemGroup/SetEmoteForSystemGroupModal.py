import discord

class SetEmoteForSystemGroupModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Set Emote for System Group")

        self.emote_input = discord.ui.InputText(label="Emote")
        self.add_item(self.emote_input)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Emote: {self.emote_input.value}", ephemeral=True)

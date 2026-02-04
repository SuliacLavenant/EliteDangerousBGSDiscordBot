import discord

class ConfirmationModal(discord.ui.Modal):
    confirmation: bool = False
    def __init__(self, title: str, confirmation_word: str):
        super().__init__(title=title)
        self.title = title
        self.confirmation_word = confirmation_word

        self.confirmation_word_input = discord.ui.InputText(
            label=f"Enter \"{confirmation_word}\" to confirm",
            placeholder=self.confirmation_word,
            required=True
            )
        self.add_item(self.confirmation_word_input)

    async def callback(self, interaction: discord.Interaction):
        text_input = self.confirmation_word_input.value

        if text_input.lower() == self.confirmation_word.lower():
            self.confirmation = True
            await interaction.response.send_message(f"{self.title}: Confirmed!",ephemeral=True)
        else:
            await interaction.response.send_message("Cases do not match, confirmation canceled.",ephemeral=True)
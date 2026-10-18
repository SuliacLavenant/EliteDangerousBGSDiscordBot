import discord

class ErrorMessageView(discord.ui.View):
    def __init__(self, error_message: str):
        super().__init__()
        self.error_message = error_message


    def get_embed(self):
        embed = discord.Embed(
            title=self.error_message
        )
        return embed

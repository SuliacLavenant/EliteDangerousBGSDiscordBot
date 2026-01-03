import discord

class ErrorMessageView(discord.ui.View):
    def __init__(self, errorMessage: str):
        super().__init__()
        self.errorMessage = errorMessage


    def getEmbed(self):
        embed = discord.Embed(
            title=self.errorMessage
        )
        return embed

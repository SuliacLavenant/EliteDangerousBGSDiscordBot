import discord

class SystemGroupDeletedView(discord.ui.View):
    def __init__(self, systemGroupName: str):
        super().__init__()
        self.systemGroupName = systemGroupName

    def getEmbed(self):
        embed = discord.Embed(
            title=f"System Group Deleted",
            description=f"System Group: **{self.systemGroupName}** succesfully deleted"
        )
        return embed

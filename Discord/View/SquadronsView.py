import discord

from DataClass.Squadron import Squadron
from DataClass.GuildSettings import GuildSettings
from PermissionManager.PermissionManager import PermissionManager


class SquadronsView(discord.ui.View):
    squadrons: list[Squadron]
    guild_id: int


    def __init__(self, squadrons: list[Squadron], guild_id: int):
        super().__init__()
        self.squadrons = squadrons
        self.guild_id = guild_id


    def get_embed(self):
        title = "Squadrons"
        description = ""
        for squadron in self.squadrons:
            description += f"{squadron.get_name_with_tag_str()}\n"
        embed = discord.Embed(title=title, description=description)

        return embed

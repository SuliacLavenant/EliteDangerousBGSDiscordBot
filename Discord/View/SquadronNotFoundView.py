import discord

from DataClass.Squadron import Squadron
from DataStorageManager import DataStorageManager
from Discord.View.SquadronView import SquadronView
from PermissionManager.PermissionManager import PermissionManager


class SquadronNotFoundView(discord.ui.View):
    guild_id: int
    squadron_name: str


    def __init__(self, squadron_name: str, guild_id: int):
        super().__init__()
        self.squadron_name = squadron_name
        self.guild_id = guild_id


    @discord.ui.button(label="Create Squadron", style=discord.ButtonStyle.primary, row=4)
    async def create_squadron(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.create(interaction.user.id, self.guild_id):
            squadron = Squadron(name=self.squadron_name)
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id)
            await interaction.response.edit_message(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        embed = discord.Embed(title="Squadron Not Found", description=f"Squadron \"**{self.squadron_name}**\" not found")
        return embed

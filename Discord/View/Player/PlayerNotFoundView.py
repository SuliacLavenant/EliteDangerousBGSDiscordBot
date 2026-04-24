import discord

from DataClass.Player import Player
from DataStorageManager import DataStorageManager
from Discord.View.Player.PlayerView import PlayerView
from PermissionManager.PermissionManager import PermissionManager


class PlayerNotFoundView(discord.ui.View):
    guild_id: int
    player_name: str


    def __init__(self, player_name: str, guild_id: int):
        super().__init__()
        self.player_name = player_name
        self.guild_id = guild_id


    @discord.ui.button(label="Create Player", style=discord.ButtonStyle.primary, row=0)
    async def create_player(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.player_permissions.create(interaction.user.id, self.guild_id):
            player = Player(name=self.player_name)
            DataStorageManager.store_player(interaction.guild_id, player)

            player = DataStorageManager.get_player_by_id(self.guild_id, player.id)
            player_view = PlayerView(player, self.guild_id)
            await interaction.response.edit_message(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        embed = discord.Embed(title="Player Not Found", description=f"Player \"**{self.player_name}**\" not found")
        return embed

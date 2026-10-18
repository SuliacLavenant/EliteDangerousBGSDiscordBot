import discord

from DataClass.Player import Player
from DataClass.GuildSettings import GuildSettings # tmp
from DatabaseGateway.DatabaseGateway import DatabaseGateway
from Discord.View.Player.PlayerView import PlayerView
from PermissionManager.PermissionManager import PermissionManager


class PlayerNotFoundView(discord.ui.View):
    discord_id: int
    player_name: str


    def __init__(self, player_name: str, discord_id: int):
        super().__init__()
        self.player_name = player_name
        self.discord_id = discord_id


    @discord.ui.button(label="Create Player", style=discord.ButtonStyle.primary, row=0)
    async def create_player(self, button: discord.ui.Button, interaction: discord.Interaction):
        #tmp, to remove later TODO
        guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.discord_id)
        if PermissionManager.player_permissions.create(interaction.user.id, guild_settings.guild_id):
            player: Player = Player(discord_id=self.discord_id,name=self.player_name)
            await DatabaseGateway.player.add(player)

            player: Player = await DatabaseGateway.player.get(self.discord_id, self.player_name)

            player_view = PlayerView(player, self.discord_id)
            await interaction.response.edit_message(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        embed = discord.Embed(title="Player Not Found", description=f"Player \"**{self.player_name}**\" not found")
        return embed

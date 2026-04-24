import discord

from DataClass.Player import Player
from DataClass.GuildSettings import GuildSettings
from DataStorageManager import DataStorageManager
from Discord.Modal.Player.RenamePlayerModal import RenamePlayerModal
from PermissionManager.PermissionManager import PermissionManager


class PlayerView(discord.ui.View):
    player: Player
    guild_id: int

    edit_mode: bool = False


    def __init__(self, player: Player, guild_id: int, edit_mode: bool = False):
        super().__init__()
        self.player = player
        self.guild_id = guild_id
        self.edit_mode = edit_mode

        if self.edit_mode:
            self.remove_item(self.edit)
        else:
            self.remove_item(self.rename)


    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary, row=0)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.player_permissions.edit(interaction.user.id, self.guild_id):
            player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
            player_view = PlayerView(player, self.guild_id, True)
            await interaction.response.edit_message(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Rename", style=discord.ButtonStyle.primary, row=0)
    async def rename(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.player_permissions.edit(interaction.user.id, self.guild_id):
            rename_player_modal = RenamePlayerModal(self.player)
            await interaction.response.send_modal(rename_player_modal)
            await rename_player_modal.wait()

            player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
            player.name = rename_player_modal.player_name
            DataStorageManager.store_player(interaction.guild_id, player)

            player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
            player_view = PlayerView(player, self.guild_id, True)
            await interaction.message.edit(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = f"{self.player.name}"
        if self.player.squadron_id != None:
            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.player.squadron_id)
            title += f" [{squadron.tag}]"
        description = ""
        embed = discord.Embed(title=title, description=description)

        return embed

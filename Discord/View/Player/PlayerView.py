import discord

from BotConfig.BotConfig import BotConfig
from DataClass.Player import Player
from DataClass.GuildSettings import GuildSettings
from DataStorageManager import DataStorageManager
from Discord.Modal.Player.RenamePlayerModal import RenamePlayerModal
from Discord.Modal.Player.SetPlayerInaraIdModal import SetPlayerInaraIdModal
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
            self.remove_item(self.set_inara_id)

        if self.player.inara_id != None:
            self.add_item(discord.ui.Button(
                label="Inara",
                url=f"https://inara.cz/elite/cmdr/{str(self.player.inara_id)}/",
                emoji="🌐",
                row=0
            ))


    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary, row=1)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.player_permissions.edit(interaction.user.id, self.guild_id):
            player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
            player_view = PlayerView(player, self.guild_id, True)
            await interaction.response.edit_message(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Rename", style=discord.ButtonStyle.primary, row=1)
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


    @discord.ui.button(label="Set Inara Id", style=discord.ButtonStyle.primary, row=1)
    async def set_inara_id(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.player_permissions.edit(interaction.user.id, self.guild_id):
            set_inara_id_player_modal = SetPlayerInaraIdModal()
            await interaction.response.send_modal(set_inara_id_player_modal)
            await set_inara_id_player_modal.wait()

            if set_inara_id_player_modal.inara_id != None:
                player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
                player.inara_id = set_inara_id_player_modal.inara_id
                DataStorageManager.store_player(interaction.guild_id, player)

            player = DataStorageManager.get_player_by_id(self.guild_id, self.player.id)
            player_view = PlayerView(player, self.guild_id, True)
            await interaction.message.edit(embed=player_view.get_embed(),view=player_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = f"{self.player.name}"
        description = ""
        embed = discord.Embed(title=title, description=description)

        ##### Accounts
        accounts_details = ""
        if self.player.discord_id != None:
            accounts_details += f"{BotConfig.indent2}**Discord**: \n"
        else:
            accounts_details += f"{BotConfig.indent2}**Discord**: Unknown\n"
        if self.player.inara_id != None:
            accounts_details += f"{BotConfig.indent2}**Inara**: [{self.player.name}](https://inara.cz/elite/cmdr/{str(self.player.inara_id)}/)"
        else:
            accounts_details += f"{BotConfig.indent2}**Inara**: Unknown"
        embed.add_field(name="Accounts", value=accounts_details, inline=False)

        ##### Squadron
        if self.player.squadron_id != None:
            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.player.squadron_id)
            squadron_details = ""
            squadron_details += f"{BotConfig.indent2}**Name**: {squadron.name}\n"
            squadron_details += f"{BotConfig.indent2}**Tag**: [{squadron.tag}]\n"
            squadron_details += f"{BotConfig.indent2}**Position in squadron**: {squadron.get_player_position_in_squadron(self.player.id)}\n"
            embed.add_field(name="Squadron", value=squadron_details, inline=False)

        return embed

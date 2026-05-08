import discord

from BotConfig.BotConfig import BotConfig
from DataClass.Squadron import Squadron
from DataClass.GuildSettings import GuildSettings
from DataStorageManager import DataStorageManager
from Discord.Modal.Squadron.AddMinorFactionToSquadronModal import AddMinorFactionToSquadronModal
from Discord.Modal.Squadron.AddPlayerToSquadronModal import AddPlayerToSquadronModal
from Discord.Modal.Squadron.RemoveMinorFactionFromSquadronModal import RemoveMinorFactionFromSquadronModal
from Discord.Modal.Squadron.RemovePlayerFromSquadronModal import RemovePlayerFromSquadronModal
from Discord.Modal.Squadron.ChangeSquadronTagModal import ChangeSquadronTagModal
from PermissionManager.PermissionManager import PermissionManager


class SquadronView(discord.ui.View):
    squadron: Squadron
    guild_id: int

    edit_mode: bool = False


    def __init__(self, squadron: Squadron, guild_id: int, edit_mode: bool = False):
        super().__init__()
        self.squadron = squadron
        self.guild_id = guild_id
        self.edit_mode = edit_mode

        if self.edit_mode:
            self.remove_item(self.edit)
            if len(self.squadron.minor_faction_names)==0:
                self.remove_minor_faction.disabled = True
        else:
            self.remove_item(self.change_tag)
            self.remove_item(self.add_minor_faction)
            self.remove_item(self.remove_minor_faction)
            self.remove_item(self.add_player_to_squadron)
            self.remove_item(self.remove_player_from_squadron)


    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary, row=0)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.edit(interaction.user.id, self.guild_id):
            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id, True)
            await interaction.response.edit_message(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Change Tag", style=discord.ButtonStyle.primary, row=0)
    async def change_tag(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.edit(interaction.user.id, self.guild_id):
            change_squadron_tag_modal = ChangeSquadronTagModal(self.squadron)
            await interaction.response.send_modal(change_squadron_tag_modal)
            await change_squadron_tag_modal.wait()

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron.tag = change_squadron_tag_modal.squadron_tag
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id, True)
            await interaction.message.edit(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Add Minor Faction", style=discord.ButtonStyle.success, row=1)
    async def add_minor_faction(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.edit(interaction.user.id, self.guild_id):
            add_minor_faction_to_squadron_modal = AddMinorFactionToSquadronModal(self.squadron)
            await interaction.response.send_modal(add_minor_faction_to_squadron_modal)
            await add_minor_faction_to_squadron_modal.wait()

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron.add_minor_faction(add_minor_faction_to_squadron_modal.minor_faction_name)
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id, True)
            await interaction.message.edit(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Remove Minor Faction", style=discord.ButtonStyle.danger, row=1)
    async def remove_minor_faction(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.edit(interaction.user.id, self.guild_id):
            remove_minor_faction_from_squadron_modal = RemoveMinorFactionFromSquadronModal(self.squadron)
            await interaction.response.send_modal(remove_minor_faction_from_squadron_modal)
            await remove_minor_faction_from_squadron_modal.wait()

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron.remove_minor_faction(remove_minor_faction_from_squadron_modal.minor_faction_name)
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id, True)
            await interaction.message.edit(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Add Player To Squadron", style=discord.ButtonStyle.success, row=2)
    async def add_player_to_squadron(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.add_player_to_squadron(interaction.user.id, self.guild_id):
            players = DataStorageManager.get_players(interaction.guild_id)
            players_without_squadron = []
            for player in players:
                if player.squadron_id == None:
                    players_without_squadron.append(player)
            add_player_to_squadron_modal = AddPlayerToSquadronModal(players_without_squadron)
            await interaction.response.send_modal(add_player_to_squadron_modal)
            await add_player_to_squadron_modal.wait()

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            for player_id in add_player_to_squadron_modal.player_id_to_add_list:
                squadron.add_player(player_id)
                player = DataStorageManager.get_player_by_id(self.guild_id, player_id)
                player.squadron_id = squadron.id
                DataStorageManager.store_player(interaction.guild_id, player)
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, self.guild_id, True)
            await interaction.message.edit(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Remove Player From Squadron", style=discord.ButtonStyle.danger, row=2)
    async def remove_player_from_squadron(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.squadron_permissions.remove_player_from_squadron(interaction.user.id, interaction.guild_id):
            squadron = DataStorageManager.get_squadron_by_id(self.guild_id, self.squadron.id)
            players = []
            for player_id in squadron.get_player_ids():
                players.append(DataStorageManager.get_player_by_id(interaction.guild_id, player_id))
            remove_player_from_squadron_modal = RemovePlayerFromSquadronModal(players)
            await interaction.response.send_modal(remove_player_from_squadron_modal)
            await remove_player_from_squadron_modal.wait()

            squadron = DataStorageManager.get_squadron_by_id(interaction.guild_id, self.squadron.id)
            for player_id in remove_player_from_squadron_modal.player_id_to_remove_list:
                squadron.remove_player(player_id)
                player = DataStorageManager.get_player_by_id(interaction.guild_id, player_id)
                player.squadron_id = None
                DataStorageManager.store_player(interaction.guild_id, player)
            DataStorageManager.store_squadron(interaction.guild_id, squadron)

            squadron = DataStorageManager.get_squadron_by_id(interaction.guild_id, self.squadron.id)
            squadron_view = SquadronView(squadron, interaction.guild_id, True)
            await interaction.message.edit(embed=squadron_view.get_embed(),view=squadron_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = f"{self.squadron.name} [{self.squadron.tag}]"
        description = ""
        if len(self.squadron.minor_faction_names) == 0:
            description += f"Minor Faction: **?**\n"
        elif len(self.squadron.minor_faction_names) == 1:
            minor_faction = DataStorageManager.get_minor_faction(self.guild_id,self.squadron.minor_faction_names[0].lower())
            if minor_faction == None:
                description += f"Minor Faction: **??{self.squadron.minor_faction_names[0].title()}??**\n"
            else:
                description += f"Minor Faction: **{minor_faction.name}**\n"
        elif len(self.squadron.minor_faction_names)>1:
            description += f"Minor Factions: "
            for minor_faction_name in self.squadron.minor_faction_names:
                minor_faction = DataStorageManager.get_minor_faction(self.guild_id,minor_faction_name.lower())
                if minor_faction == None:
                    description += f"**??{minor_faction_name.title()}??**, "
                else:
                    description += f"**{minor_faction.name}**, "
            description += f"\n"
        embed = discord.Embed(title=title, description=description)

        #players
        if len(self.squadron.leader_ids)>0:
            players = ""
            for player_id in self.squadron.recruit_ids:
                emote = BotConfig.emotes.squadron.members.leader
                player = DataStorageManager.get_player_by_id(self.guild_id, player_id)
                players += f"{BotConfig.indent2}{emote} {player.name}\n"
            embed.add_field(name="Leaders", value=players, inline=False)
        if len(self.squadron.officer_ids)>0:
            players = ""
            for player_id in self.squadron.recruit_ids:
                emote = BotConfig.emotes.squadron.members.officer
                player = DataStorageManager.get_player_by_id(self.guild_id, player_id)
                players += f"{BotConfig.indent2}{emote} {player.name}\n"
            embed.add_field(name="Officers", value=players, inline=False)
        if len(self.squadron.member_ids)>0:
            players = ""
            for player_id in self.squadron.recruit_ids:
                emote = BotConfig.emotes.squadron.members.member
                player = DataStorageManager.get_player_by_id(self.guild_id, player_id)
                players += f"{BotConfig.indent2}{emote} {player.name}\n"
            embed.add_field(name="Members", value=players, inline=False)
        if len(self.squadron.recruit_ids)>0:
            players = ""
            for player_id in self.squadron.recruit_ids:
                emote = BotConfig.emotes.squadron.members.recruit
                player = DataStorageManager.get_player_by_id(self.guild_id, player_id)
                players += f"{BotConfig.indent2}{emote} {player.name}\n"
            embed.add_field(name="Recruits", value=players, inline=False)

        return embed

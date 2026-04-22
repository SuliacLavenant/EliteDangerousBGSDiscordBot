import discord

from DataClass.Squadron import Squadron
from DataClass.GuildSettings import GuildSettings
from DataStorageManager import DataStorageManager
from Discord.Modal.Squadron.AddMinorFactionToSquadronModal import AddMinorFactionToSquadronModal
from Discord.Modal.Squadron.RemoveMinorFactionFromSquadronModal import RemoveMinorFactionFromSquadronModal
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
            embed.add_field(name="Leaders", value="list of leaders", inline=False)
        if len(self.squadron.officer_ids)>0:
            embed.add_field(name="Officers", value="list of Officers", inline=False)
        if len(self.squadron.member_ids)>0:
            embed.add_field(name="Members", value="list of Members", inline=False)
        if len(self.squadron.recruit_ids)>0:
            embed.add_field(name="Recruits", value="list of Recruits", inline=False)

        return embed

import discord

from DataClass.SystemGroup import SystemGroup
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from Discord.Modal.ConfirmationModal import ConfirmationModal
from Discord.Modal.SystemGroup.SetColorForSystemGroupModal import SetColorForSystemGroupModal
from Discord.Modal.SystemGroup.SetEmoteForSystemGroupModal import SetEmoteForSystemGroupModal
from Discord.View.SystemGroup.SelectSystemsToAddToGroupView import SelectSystemsToAddToGroupView
from PermissionManager.PermissionManager import PermissionManager

class SystemGroupView(discord.ui.View):
    def __init__(self, system_group: SystemGroup):
        super().__init__()
        self.system_group = system_group


    @discord.ui.button(label="Set Color", style=discord.ButtonStyle.secondary, emoji="🖌️", row=0)
    async def set_color(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.set_color(interaction.user.id):
            set_color_for_system_group_modal = SetColorForSystemGroupModal()
            await interaction.response.send_modal(set_color_for_system_group_modal)
            await set_color_for_system_group_modal.wait()

            self.system_group = DataStorageManager.getSystemGroup(interaction.guild_id,self.system_group.name)

            if set_color_for_system_group_modal.color != None:
                self.system_group.set_rgb_color(set_color_for_system_group_modal.color.to_rgb())

            DataStorageManager.storeSystemGroup(interaction.guild_id,self.system_group)

            system_group_view = SystemGroupView(self.system_group)
            await interaction.edit_original_response(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Emote", style=discord.ButtonStyle.secondary, emoji="🙂", row=0)
    async def set_emote(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.set_emote(interaction.user.id):
            set_emote_for_system_group_modal = SetEmoteForSystemGroupModal()
            await interaction.response.send_modal(set_emote_for_system_group_modal)
            await set_emote_for_system_group_modal.wait()

            self.system_group = DataStorageManager.getSystemGroup(interaction.guild_id,self.system_group.name)
            self.system_group.emote = str(set_emote_for_system_group_modal.emote_input.value)
            DataStorageManager.storeSystemGroup(interaction.guild_id,self.system_group)

            system_group_view = SystemGroupView(self.system_group)
            await interaction.edit_original_response(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Add systems to group", style=discord.ButtonStyle.secondary, emoji="➕", row=1)
    async def add_systems_to_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.add_systems(interaction.user.id):
            system_name_list = DataManager.getSystemNamesWithNoGroupList(interaction.guild_id)
            system_name_list.sort()
            if system_name_list!=None and len(system_name_list)>0:
                select_systems_to_add_to_group_view = SelectSystemsToAddToGroupView(self.system_group,system_name_list)
                await interaction.response.edit_message(embed=select_systems_to_add_to_group_view.get_embed(),view=select_systems_to_add_to_group_view)
            else:
                await interaction.response.send_message(f"All systems are already in a group", ephemeral=True)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Delete System Group", style=discord.ButtonStyle.danger, emoji="🗑️", row=2)
    async def delete_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.delete(interaction.user.id):
            confirmation_modal = ConfirmationModal(f"Delete System Group \"{self.system_group.name}\"",self.system_group.name)
            await interaction.response.send_modal(confirmation_modal)
            await confirmation_modal.wait()

            if confirmation_modal.confirmation:
                DataStorageManager.removeSystemGroup(interaction.guild_id,self.system_group.name)

                from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
                system_groups_view = SystemGroupsView(DataManager.getSystemGroups(interaction.guild_id))
                await interaction.message.edit(embed=system_groups_view.get_embed(), view=system_groups_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = ""
        if self.system_group.emote!=None:
            title += f"{self.system_group.emote} {self.system_group.name} {self.system_group.emote}"
        else:
            title += f"{self.system_group.name}"

        description="Systems:"
        for systemName in self.system_group.systems:
                description += f"\n{systemName}"
        
        if self.system_group.rgb_color!=None:
            embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(self.system_group.rgb_color[0],self.system_group.rgb_color[1],self.system_group.rgb_color[2]))
        else:
            embed = discord.Embed(title=title, description=description)

        return embed

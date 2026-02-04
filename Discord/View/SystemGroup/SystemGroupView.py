import discord

from DataClass.SystemGroup import SystemGroup
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from Discord.View.SystemGroup.Edit.SelectSystemsToAddToGroupView import SelectSystemsToAddToGroupView
from Discord.Modal.ConfirmationModal import ConfirmationModal
from Discord.Modal.SystemGroup.SetEmoteForSystemGroupModal import SetEmoteForSystemGroupModal
from PermissionManager.PermissionManager import PermissionManager

class SystemGroupView(discord.ui.View):
    def __init__(self, system_group: SystemGroup):
        super().__init__()
        self.system_group = system_group


    @discord.ui.button(label="Set Emote For System Group", style=discord.ButtonStyle.secondary, emoji="🙂", row=0)
    async def set_emote_for_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.set_emote(interaction.user.id):
            set_emote_for_system_group_modal = SetEmoteForSystemGroupModal()
            await interaction.response.send_modal(set_emote_for_system_group_modal)
            await set_emote_for_system_group_modal.wait()

            self.system_group = DataStorageManager.getSystemGroup(interaction.guild_id,self.system_group.name)
            self.system_group.emote = str(set_emote_for_system_group_modal.emote_input.value)
            DataStorageManager.storeSystemGroup(interaction.guild_id,self.system_group)

            system_group_view = SystemGroupView(self.system_group)
            await interaction.message.edit(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)
    

    @discord.ui.button(label="Add Systems to SystemGroup", style=discord.ButtonStyle.secondary, row=1)
    async def addSystemsToSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.add_systems(interaction.user.id):
            systemNameList = DataManager.getSystemNamesWithNoGroupList(interaction.guild_id)
            systemNameList.sort()
            if systemNameList!=None and len(systemNameList)>0:
                selectSystemsToAddToGroupView = SelectSystemsToAddToGroupView(self.system_group,systemNameList)
                await interaction.response.edit_message(embed=selectSystemsToAddToGroupView.getEmbed(),view=selectSystemsToAddToGroupView)
            else:
                systemGroupView = SystemGroupView(self.system_group)
                await interaction.response.edit_message(embed=systemGroupView.getEmbed(),view=systemGroupView)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Delete SystemGroup", style=discord.ButtonStyle.danger, row=2)
    async def delete_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.delete(interaction.user.id):
            confirmation_modal = ConfirmationModal(f"Delete System Group \"{self.system_group.name}\"",self.system_group.name)
            await interaction.response.send_modal(confirmation_modal)
            await confirmation_modal.wait()

            if confirmation_modal.confirmation:
                DataStorageManager.removeSystemGroup(interaction.guild_id,self.system_group.name)

                from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
                systemGroupsView = SystemGroupsView(DataManager.getSystemGroups(interaction.guild_id))
                await interaction.message.edit(embed=systemGroupsView.get_embed(), view=systemGroupsView)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = "System Group: "
        if self.system_group.emote!=None:
            title += f"{self.system_group.emote} {self.system_group.name} {self.system_group.emote}"
        else:
            title += f"{self.system_group.name}"

        description="Systems:"
        for systemName in self.system_group.systems:
                description += f"\n{systemName}"

        embed = discord.Embed(title=title, description=description)
        return embed

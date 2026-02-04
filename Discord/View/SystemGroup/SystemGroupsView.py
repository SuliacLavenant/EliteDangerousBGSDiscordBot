import discord

from BotConfig.BotConfig import BotConfig
from DataClass.SystemGroup import SystemGroup
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from Discord.Modal.SystemGroup.CreateSystemGroupModal import CreateSystemGroupModal
from Discord.View.SystemGroup.SystemGroupView import SystemGroupView
from PermissionManager.PermissionManager import PermissionManager

class SystemGroupsView(discord.ui.View):
    def __init__(self, system_groups):
        super().__init__()
        self.system_groups = system_groups

        select_options = []
        for systemGroup in self.system_groups:
            select_option = discord.SelectOption(label=systemGroup.name)
            select_options.append(select_option)
        
        self.select = discord.ui.Select(
            placeholder = f"Select a System Group",
            min_values = 1,
            max_values = 1,
            options = select_options,
            row = 1
        )
        self.select.callback = self.select_system_group_callback
        self.add_item(self.select)


    @discord.ui.button(label="Create New Group", style=discord.ButtonStyle.success,row=2)
    async def create_new_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.create(interaction.user.id):
            create_system_group_modal = CreateSystemGroupModal()
            await interaction.response.send_modal(create_system_group_modal)
            await create_system_group_modal.wait()

            if create_system_group_modal.new_system_group:
                system_group_name = str(create_system_group_modal.system_group_name_input.value)
                system_group = SystemGroup(name=system_group_name)
                DataStorageManager.storeSystemGroup(interaction.guild_id, system_group)

                system_group_view = SystemGroupView(system_group)
                await interaction.message.edit(embed=system_group_view.get_embed(), view=system_group_view)


    def get_embed(self):
        title = "Manage System Groups"
        description = f"Number of Groups: {len(self.system_groups)}"
        embed = discord.Embed(title=title, description=description)

        for system_group in self.system_groups:
            name = system_group.name
            if system_group.emote!=None:
                name = f"{system_group.emote} {system_group.name} {system_group.emote}"

            embed.add_field(name=name, value=f"{BotConfig.emotesN.systems} {len(system_group.systems)} systems", inline=False)

        return embed


    async def select_system_group_callback(self, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.see(interaction.user.id):
            selected = self.select.values[0]
            system_group_view = SystemGroupView(DataManager.getSystemGroup(interaction.guild_id,selected))
            await interaction.response.edit_message(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)

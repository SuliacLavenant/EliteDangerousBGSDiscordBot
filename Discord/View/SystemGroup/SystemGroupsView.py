import discord

from BotConfig.BotConfig import BotConfig
from DatabaseGateway.DatabaseGateway import DatabaseGateway
from DataClass.GuildSettings import GuildSettings
from DataClass.SystemGroup import SystemGroup
from DataManager import DataManager
# from DataStorageManager import DataStorageManager
from Discord.Modal.SystemGroup.CreateSystemGroupModal import CreateSystemGroupModal
from Discord.View.SystemGroup.SystemGroupView import SystemGroupView
from PermissionManager.PermissionManager import PermissionManager

class SystemGroupsView(discord.ui.View):
    def __init__(self, system_groups: list, guild_settings: GuildSettings):
        super().__init__()
        self.system_groups = system_groups
        self.guild_settings = guild_settings

        if len(self.system_groups) >= 1:
            select_options = []
            for system_group in self.system_groups:
                select_option = discord.SelectOption(label=system_group.name, value=str(system_group.id))
                select_options.append(select_option)
            
            self.select = discord.ui.Select(
                placeholder = f"Select a Group",
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
            create_system_group_modal: CreateSystemGroupModal = CreateSystemGroupModal()
            await interaction.response.send_modal(create_system_group_modal)
            await create_system_group_modal.wait()
            system_group_name = create_system_group_modal.system_group_name

            name_already_used: bool = False
            for system_group in self.system_groups:
                if system_group.name == system_group_name:
                    name_already_used = True
                    break

            if not name_already_used and system_group_name != "":
                system_group = SystemGroup(name=system_group_name, discord_id=self.guild_settings.id)
                success: bool = await DatabaseGateway.system_group.add(system_group)
                if success:
                    system_group = await DatabaseGateway.system_group.get_by_name(self.guild_settings.id, system_group_name)
                    guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
                    system_group_view = SystemGroupView(system_group, guild_settings)
                    await interaction.edit_original_response(embed=system_group_view.get_embed(), view=system_group_view)

            else:
                await interaction.followup.send(f"System Group \"{system_group_name}\" already exist!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def get_embed(self):
        title = "Manage System Groups"
        description = f"Number of Groups: {len(self.system_groups)}"
        embed = discord.Embed(title=title, description=description)

        for system_group in self.system_groups:
            name = system_group.name
            if system_group.emote!=None:
                name = f"{system_group.emote} {system_group.name} {system_group.emote}"
            text = f"{BotConfig.emotes.systems} Systems: {len(system_group.systems)}"
            embed.add_field(name=name, value=text, inline=False)

        return embed

    #TODO maybe security issue if not checked that system group is owned by the discord
    async def select_system_group_callback(self, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.see(interaction.user.id):
            selected_id: int = int(self.select.values[0])
            system_group = await DatabaseGateway.system_group.get(selected_id)
            guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
            system_group_view = SystemGroupView(system_group,guild_settings)
            await interaction.response.edit_message(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)

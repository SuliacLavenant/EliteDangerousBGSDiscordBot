import discord

from BotConfig.BotConfig import BotConfig
from DatabaseGateway.DatabaseGateway import DatabaseGateway
from DataClass.GuildSettings import GuildSettings
from DataClass.SystemGroup import SystemGroup
from DataManager import DataManager
# from DataStorageManager import DataStorageManager
from Discord.Modal.ConfirmationModal import ConfirmationModal
from Discord.Modal.SystemGroup.RenameSystemGroupModal import RenameSystemGroupModal
from Discord.Modal.SystemGroup.SelectSystemsToAddToSystemGroupModal import SelectSystemsToAddToSystemGroupModal
from Discord.Modal.SystemGroup.SelectSystemsToRemoveFromSystemGroupModal import SelectSystemsToRemoveFromSystemGroupModal
from Discord.Modal.SystemGroup.SetColorForSystemGroupModal import SetColorForSystemGroupModal
from Discord.Modal.SystemGroup.SetEmoteForSystemGroupModal import SetEmoteForSystemGroupModal
from PermissionManager.PermissionManager import PermissionManager


class SystemGroupView(discord.ui.View):
    def __init__(self, system_group: SystemGroup, guild_settings: GuildSettings):
        super().__init__()
        self.system_group = system_group
        self.guild_settings = guild_settings

        if len(self.system_group.systems) == 0:
            self.remove_systems_from_system_group.disabled = True
        else:
            self.delete_system_group.disabled = True


    @discord.ui.button(label="Set Color", style=discord.ButtonStyle.secondary, emoji="🖌️", row=0)
    async def set_color(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.set_color(interaction.user.id):
            set_color_for_system_group_modal: SetColorForSystemGroupModal = SetColorForSystemGroupModal()
            await interaction.response.send_modal(set_color_for_system_group_modal)
            await set_color_for_system_group_modal.wait()

            if set_color_for_system_group_modal.color != None:
                color_rgb: tuple = set_color_for_system_group_modal.color.to_rgb()
                color_rgb_list: list = [color_rgb[0],color_rgb[1],color_rgb[2]]
                success: bool = await DatabaseGateway.system_group.set_color(self.system_group.id, color_rgb_list)

            system_group = await DatabaseGateway.system_group.get(self.system_group.id)
            guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
            system_group_view = SystemGroupView(system_group, guild_settings)
            await interaction.edit_original_response(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Set Emote", style=discord.ButtonStyle.secondary, emoji="🙂", row=0)
    async def set_emote(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.set_emote(interaction.user.id):
            set_emote_for_system_group_modal = SetEmoteForSystemGroupModal()
            await interaction.response.send_modal(set_emote_for_system_group_modal)
            await set_emote_for_system_group_modal.wait()

            success: bool = await DatabaseGateway.system_group.set_emote(self.system_group.id, set_emote_for_system_group_modal.emote)

            system_group = await DatabaseGateway.system_group.get(self.system_group.id)
            guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
            system_group_view = SystemGroupView(system_group, guild_settings)
            await interaction.edit_original_response(embed=system_group_view.get_embed(), view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Add systems", style=discord.ButtonStyle.secondary, emoji="➕", row=1)
    async def add_systems_to_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.add_systems(interaction.user.id):
            guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id, True)
            tracked_systems: list = guild_settings.get_tracked_system_with_no_group()

            if len(tracked_systems)>0:
                select_systems_to_add_to_system_group_modal: SelectSystemsToAddToSystemGroupModal = SelectSystemsToAddToSystemGroupModal(tracked_systems)
                await interaction.response.send_modal(select_systems_to_add_to_system_group_modal)
                await select_systems_to_add_to_system_group_modal.wait()

                for tracked_system in tracked_systems:
                    if tracked_system.system.name in select_systems_to_add_to_system_group_modal.system_names_to_add:
                        await DatabaseGateway.discord_tracked_system.add_to_system_group(tracked_system.discord_id, tracked_system.system_id, self.system_group.id)

                system_group = await DatabaseGateway.system_group.get(self.system_group.id)
                guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
                system_group_view = SystemGroupView(system_group, guild_settings)
                await interaction.edit_original_response(embed=system_group_view.get_embed(), view=system_group_view)
            else:
                await interaction.response.send_message(f"All systems are already in a group", ephemeral=True)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    #disabled if no systems
    @discord.ui.button(label="Remove systems", style=discord.ButtonStyle.secondary, emoji="➖", row=1)
    async def remove_systems_from_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.remove_systems(interaction.user.id):
            select_systems_to_remove_from_system_group_modal = SelectSystemsToRemoveFromSystemGroupModal(self.system_group.systems)
            await interaction.response.send_modal(select_systems_to_remove_from_system_group_modal)
            await select_systems_to_remove_from_system_group_modal.wait()

            for tracked_system in self.system_group.systems:
                if tracked_system.system.name in select_systems_to_remove_from_system_group_modal.system_names_to_remove:
                    await DatabaseGateway.discord_tracked_system.remove_from_system_group(tracked_system.discord_id, tracked_system.system_id)

            system_group = await DatabaseGateway.system_group.get(self.system_group.id)
            guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
            system_group_view = SystemGroupView(system_group, guild_settings)
            await interaction.edit_original_response(embed=system_group_view.get_embed(),view=system_group_view)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Rename", style=discord.ButtonStyle.secondary, emoji="✍🏼", row=0)
    async def rename_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.rename(interaction.user.id):
            rename_system_group_modal: RenameSystemGroupModal = RenameSystemGroupModal()
            await interaction.response.send_modal(rename_system_group_modal)
            await rename_system_group_modal.wait()

            success: bool = False
            if rename_system_group_modal.system_group_new_name != "":
                system_group_with_that_name: SystemGroup = await DatabaseGateway.system_group.get_by_name(self.guild_settings.id,rename_system_group_modal.system_group_new_name)
                if system_group_with_that_name is None:
                    success = await DatabaseGateway.system_group.rename(self.system_group.id, rename_system_group_modal.system_group_new_name)

            if success:
                system_group = await DatabaseGateway.system_group.get(self.system_group.id)
                guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get(self.guild_settings.id)
                system_group_view = SystemGroupView(system_group, guild_settings)
                await interaction.edit_original_response(embed=system_group_view.get_embed(), view=system_group_view)
            else:
                await interaction.followup.send(f"System Group \"{rename_system_group_modal.system_group_new_name}\" already exist!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, emoji="🗑️", row=2)
    async def delete_system_group(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.system_group_permissions.delete(interaction.user.id):
            confirmation_modal = ConfirmationModal(f"Delete System Group \"{self.system_group.name}\"",self.system_group.name)
            await interaction.response.send_modal(confirmation_modal)
            await confirmation_modal.wait()

            if confirmation_modal.confirmation:
                await DatabaseGateway.system_group.delete(self.system_group.id) #TODO delete system_group_system before

                guild_settings: GuildSettings = await DatabaseGateway.guild_settings.get_from_guild_id(interaction.guild_id)
                system_groups: list = await DatabaseGateway.system_group.get_all_from_discord(guild_settings.id)

                from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
                system_groups_view = SystemGroupsView(system_groups, guild_settings)
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
        system_names: list[str] = []
        for tracked_system in self.system_group.systems:
            system_names.append(tracked_system.system.name)
        system_names.sort()
        for system_name in system_names:
            description += f"\n{BotConfig.indent2} {system_name}"
        
        if self.system_group.color_rgb!=None:
            embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(self.system_group.color_rgb[0],self.system_group.color_rgb[1],self.system_group.color_rgb[2]))
        else:
            embed = discord.Embed(title=title, description=description)

        return embed

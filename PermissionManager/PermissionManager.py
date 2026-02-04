import discord
from discord.ext import commands

from PermissionManager.GuildSettingsPermissions import GuildSettingsPermissions
from PermissionManager.SystemGroupPermissions import SystemGroupPermissions

class PermissionManager:
    super_admin_id: int | None = None
    guild_settings_permissions = GuildSettingsPermissions
    system_group_permissions = SystemGroupPermissions


    @classmethod
    def set_super_admin_id(cls, user_id):
        cls.super_admin_id = user_id
        cls.guild_settings_permissions.set_super_admin_id(user_id)
        cls.system_group_permissions.set_super_admin_id(user_id)

    @classmethod
    def is_user_super_admin(cls, user_id: int) -> bool:
        return cls.super_admin_id is not None and cls.super_admin_id == user_id

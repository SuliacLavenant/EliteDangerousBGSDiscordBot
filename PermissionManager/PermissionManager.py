import discord
from discord.ext import commands

from PermissionManager.GuildSettingsPermissions import GuildSettingsPermissions
from PermissionManager.MissionPermissions import MissionPermissions
from PermissionManager.PlayerPermissions import PlayerPermissions
from PermissionManager.SquadronPermissions import SquadronPermissions
from PermissionManager.SystemGroupPermissions import SystemGroupPermissions

class PermissionManager:
    super_admin_id: int | None = None

    guild_settings_permissions = GuildSettingsPermissions
    mission_permissions = MissionPermissions
    player_permissions = PlayerPermissions
    squadron_permissions = SquadronPermissions
    system_group_permissions = SystemGroupPermissions


    @classmethod
    def set_super_admin_id(cls, user_id):
        cls.super_admin_id = user_id
        cls.guild_settings_permissions.set_super_admin_id(user_id)
        cls.mission_permissions.set_super_admin_id(user_id)
        cls.player_permissions.set_super_admin_id(user_id)
        cls.squadron_permissions.set_super_admin_id(user_id)
        cls.system_group_permissions.set_super_admin_id(user_id)


    @classmethod
    def is_user_super_admin(cls, user_id: int) -> bool:
        return cls.super_admin_id is not None and cls.super_admin_id == user_id

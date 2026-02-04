import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class GuildSettingsPermissions(AbstractPermissions):

    @classmethod
    def see(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def set_channel(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)



################ Predicates
    @classmethod
    def see_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.see(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def set_channel_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.set_channel(ctx.author.id)
        return commands.check(predicate)
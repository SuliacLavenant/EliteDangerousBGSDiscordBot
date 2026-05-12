import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class SystemPermissions(AbstractPermissions):

    @classmethod
    def set_architect(cls, user_id: int) -> bool:
        return cls.is_user_super_admin(user_id)


################ Predicates
    @classmethod
    def set_architect_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.set_architect(ctx.author.id)
        return commands.check(predicate)

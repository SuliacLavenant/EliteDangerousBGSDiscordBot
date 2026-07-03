import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class SystemPermissions(AbstractPermissions):

    @classmethod
    def set_architect(cls, user_id: int) -> bool:
        return cls.is_user_super_admin(user_id)


    @classmethod
    def store(cls, user_id: int) -> bool:
        return cls.is_user_super_admin(user_id)


    @classmethod
    def unstore(cls, user_id: int) -> bool:
        return cls.is_user_super_admin(user_id)


################ Predicates
    @classmethod
    def set_architect_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.set_architect(ctx.author.id)
        return commands.check(predicate)


    @classmethod
    def store_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.store(ctx.author.id)
        return commands.check(predicate)


    @classmethod
    def unstore_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.unstore(ctx.author.id)
        return commands.check(predicate)

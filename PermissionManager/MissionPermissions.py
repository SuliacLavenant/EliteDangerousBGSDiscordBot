import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class MissionPermissions(AbstractPermissions):

    @classmethod
    def create(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)



################ Predicates
    @classmethod
    def create_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.create(ctx.author.id)
        return commands.check(predicate)
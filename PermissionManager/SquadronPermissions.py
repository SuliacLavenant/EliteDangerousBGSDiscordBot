import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class SquadronPermissions(AbstractPermissions):

    @classmethod
    def create(cls, user_id, guild_id) -> bool:
        return cls.is_user_super_admin(user_id)


    @classmethod
    def edit(cls, user_id, guild_id) -> bool:
        return cls.is_user_super_admin(user_id)


    @classmethod
    def see(cls, user_id, guild_id) -> bool:
        return cls.is_user_super_admin(user_id)



################ Predicates
    @classmethod
    def create_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.create(ctx.author.id, ctx.guild_id)
        return commands.check(predicate)


    @classmethod
    def edit_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.edit(ctx.author.id, ctx.guild_id)
        return commands.check(predicate)


    @classmethod
    def see_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.see(ctx.author.id, ctx.guild_id)
        return commands.check(predicate)

import discord
from discord.ext import commands

from PermissionManager.AbstractPermissions import AbstractPermissions

class SystemGroupPermissions(AbstractPermissions):

    @classmethod
    def add_systems(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def create(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def delete(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def see(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def see_list(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)

    @classmethod
    def set_emote(cls, user_id) -> bool:
        return cls.is_user_super_admin(user_id)



################ Predicates

    @classmethod
    def add_systems_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.add_systems(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def create_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.create(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def delete_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.delete(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def see_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.see(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def see_list_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.see_list(ctx.author.id)
        return commands.check(predicate)

    @classmethod
    def set_emote_predicate(cls):
        async def predicate(ctx: discord.ApplicationContext) -> bool:
            return cls.set_emote(ctx.author.id)
        return commands.check(predicate)

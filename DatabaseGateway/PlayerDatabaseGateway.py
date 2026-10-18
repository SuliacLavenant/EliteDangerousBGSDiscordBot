import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.Player import Player


class PlayerDatabaseGateway:
    def __init__(self, Session):
        self.Session = Session


    async def add(self, player: Player):
        if not await self.exists(player.discord_id, player.name):
            async with self.Session() as session:
                try:
                    session.add(player)
                    await session.commit()
                except IntegrityError:
                    await session.rollback()
                    return False

                return True
        else:
            return False


    async def exists(self, discord_id: int, player_name: str):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where((Player.discord_id == discord_id) & (Player.name == player_name))
                )
            )

            return result


    async def force_update(self, player: Player):
        async with self.Session() as session:
            try:
                await session.merge(player)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get(self, discord_id: int, player_name: str):
        player: Player = None
        async with self.Session() as session:
            result = await session.execute(
                select(Player)
                .where((Player.discord_id == discord_id) & (Player.name == player_name))
            )
            player = result.scalar_one_or_none()

        return player


    ######################################

    # async def set_bgs_change_log_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
    #     async with self.Session() as session:
    #         result = await session.execute(
    #             select(GuildSettings)
    #             .where(GuildSettings.id == guild_settings_id)
    #         )
    #         guild_settings: GuildSettings = result.scalar_one_or_none()
    #         if guild_settings is None:
    #             return None

    #         guild_settings.bgs_change_log_channel_id = channel_id

    #         await session.commit()
    #         await session.refresh(guild_settings)
        
    #         return guild_settings


    # async def add_trusted_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
    #     async with self.Session() as session:
    #         result = await session.execute(
    #             select(GuildSettings)
    #             .where(GuildSettings.id == guild_settings_id)
    #         )
    #         guild_settings: GuildSettings = result.scalar_one_or_none()
    #         if guild_settings is None:
    #             return None

    #         if channel_id not in guild_settings.trusted_channel_ids:
    #             guild_settings.trusted_channel_ids.append(channel_id)

    #         await session.commit()
    #         await session.refresh(guild_settings)
        
    #         return guild_settings


    # async def remove_trusted_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
    #     async with self.Session() as session:
    #         result = await session.execute(
    #             select(GuildSettings)
    #             .where(GuildSettings.id == guild_settings_id)
    #         )
    #         guild_settings: GuildSettings = result.scalar_one_or_none()
    #         if guild_settings is None:
    #             return None

    #         if channel_id in guild_settings.trusted_channel_ids:
    #             guild_settings.trusted_channel_ids.remove(channel_id)

    #         await session.commit()
    #         await session.refresh(guild_settings)
        
    #         return guild_settings

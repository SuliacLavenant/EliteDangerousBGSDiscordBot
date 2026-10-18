import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload


from DataClass.GuildSettings import GuildSettings
from DataClass.SystemGroup import SystemGroup


class GuildSettingsDatabaseGateway:
    def __init__(self, Session):
        self.Session = Session


    async def add(self, guild_settings: GuildSettings):
        async with self.Session() as session:
            try:
                session.add(guild_settings)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def exists(self, guild_id: int):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(GuildSettings.guild_id == guild_id)
                )
            )

            return result


    async def force_update(self, guild_settings: GuildSettings):
        async with self.Session() as session:
            try:
                await session.merge(guild_settings)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get_from_guild_id(self, guild_id: int):
        guild_settings: GuildSettings = None
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.guild_id == guild_id)
            )
            guild_settings = result.scalar_one_or_none()

        return guild_settings


    async def get(self, id: int, tracked_systems: bool = False, system_groups: bool = False, minor_faction: bool = False):
        async with self.Session() as session:
            options = []
            if tracked_systems:
                options.append(
                    selectinload(GuildSettings.tracked_systems)
                )
            if system_groups:
                options.append(
                    selectinload(GuildSettings.system_groups)
                    .selectinload(SystemGroup.systems)
                )
            if minor_faction:
                options.append(
                    selectinload(GuildSettings.minor_faction)
                )

            guild_settings: GuildSettings = await session.get(
                GuildSettings,
                (id),
                options=options
            )

            return guild_settings


    ######################################

    async def set_minor_faction_id(self, guild_settings_id: int, minor_faction_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            guild_settings: GuildSettings = await session.get(
                GuildSettings,
                (guild_settings_id)
            )
            if guild_settings is None:
                return False

            guild_settings.minor_faction_id = minor_faction_id
            await session.commit()
            return True


    ###################################### channels

    async def set_bgs_change_log_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            guild_settings.bgs_change_log_channel_id = channel_id

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings


    async def set_mission_recap_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            guild_settings.mission_recap_channel_id = channel_id

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings


    async def set_bgs_system_recap_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            guild_settings.bgs_system_recap_channel_id = channel_id

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings


    async def set_bgs_warning_recap_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            guild_settings.bgs_warning_recap_channel_id = channel_id

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings


    async def add_trusted_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            if channel_id not in guild_settings.trusted_channel_ids:
                guild_settings.trusted_channel_ids.append(channel_id)

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings


    async def remove_trusted_channel_id(self, guild_settings_id: int, channel_id: int) -> GuildSettings | None:
        async with self.Session() as session:
            result = await session.execute(
                select(GuildSettings)
                .where(GuildSettings.id == guild_settings_id)
            )
            guild_settings: GuildSettings = result.scalar_one_or_none()
            if guild_settings is None:
                return None

            if channel_id in guild_settings.trusted_channel_ids:
                guild_settings.trusted_channel_ids.remove(channel_id)

            await session.commit()
            await session.refresh(guild_settings)
        
            return guild_settings

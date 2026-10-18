import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.DiscordTrackedSystem import DiscordTrackedSystem


class DiscordTrackedSystemDatabaseGateway:

    def __init__(self, Session):
        self.Session = Session


    async def exists(self, discord_id: int, system_id: int):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(
                        DiscordTrackedSystem.discord_id == discord_id,
                        DiscordTrackedSystem.system_id == system_id
                    )
                )
            )

            return result


    async def add(self, discord_tracked_system: DiscordTrackedSystem) -> bool:
        async with self.Session() as session:
            try:
                session.add(discord_tracked_system)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def force_update(self, discord_tracked_system: DiscordTrackedSystem):
        async with self.Session() as session:
            try:
                await session.merge(discord_tracked_system)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get(self, discord_id: int, system_id: int):
        async with self.Session() as session:
            return await session.get(
                DiscordTrackedSystem,
                (discord_id, system_id)
            )


    async def delete(self, discord_id: int, system_id: int):
        async with self.Session() as session:
            try:
                discord_tracked_system: DiscordTrackedSystem = await session.get(
                    DiscordTrackedSystem,
                    (discord_id, system_id)
                )
                if discord_tracked_system == None:
                    return False
                else:
                    await session.delete(discord_tracked_system)
                    await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


#####################################


    async def add_to_system_group(self, discord_id: int, system_id: int, system_group_id: int) -> bool:
        async with self.Session() as session:
            discord_tracked_system: DiscordTrackedSystem = await session.get(
                DiscordTrackedSystem,
                (discord_id, system_id)
            )
            if discord_tracked_system is None:
                return False

            discord_tracked_system.system_group_id = system_group_id

            await session.commit()
            return True


    async def remove_from_system_group(self, discord_id: int, system_id: int) -> bool:
        async with self.Session() as session:
            discord_tracked_system: DiscordTrackedSystem = await session.get(
                DiscordTrackedSystem,
                (discord_id, system_id)
            )
            if discord_tracked_system is None:
                return False

            discord_tracked_system.system_group_id = None

            await session.commit()
            return True

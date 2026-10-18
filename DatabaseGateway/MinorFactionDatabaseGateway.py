import asyncio
import selectors
from sqlalchemy import func, select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.MinorFaction import MinorFaction


class MinorFactionDatabaseGateway:

    def __init__(self, Session):
        self.Session = Session


    async def exists(self, minor_faction_name: str):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(MinorFaction.name == minor_faction_name)
                )
            )

            return result


    async def add(self, minor_faction: MinorFaction):
        async with self.Session() as session:
            try:
                session.add(minor_faction)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def force_update(self, minor_faction: MinorFaction):
        async with self.Session() as session:
            try:
                await session.merge(minor_faction)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get_by_name(self, minor_faction_name: str):
        minor_faction: MinorFaction = None
        async with self.Session() as session:
            result = await session.execute(
                select(MinorFaction)
                .where(func.lower(MinorFaction.name) == minor_faction_name.lower())
            )
            minor_faction = result.scalar_one_or_none()
            if minor_faction is not None:
                await session.refresh(minor_faction, ["origin_system","system_minor_faction_details_list"])

        return minor_faction


    async def get(self, id: int):
        async with self.Session() as session:
            minor_faction: MinorFaction = await session.get(
                MinorFaction,
                (id)
            )
            return minor_faction


    async def delete(self, minor_faction_name: str):
        return False # safety
        async with self.Session() as session:
            try:
                result = await session.execute(
                    select(MinorFaction)
                    .where(MinorFaction.name == minor_faction_name)
                )
                minor_faction = result.scalar_one_or_none()
                if minor_faction == None:
                    return False
                else:
                    await session.delete(minor_faction)
                    await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def set_name(self, id: int, name: str) -> System | None:
        async with self.Session() as session:
            minor_faction: MinorFaction = await session.get(
                MinorFaction,
                (id)
            )
            if minor_faction is None:
                return False

            minor_faction.name = name

            await session.commit()        
            return True

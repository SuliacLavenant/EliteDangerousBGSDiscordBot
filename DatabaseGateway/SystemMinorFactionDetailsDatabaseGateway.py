import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.SystemMinorFactionDetails import SystemMinorFactionDetails


class SystemMinorFactionDetailsDatabaseGateway:

    def __init__(self, Session):
        self.Session = Session


    async def exists(self, system_id: int, minor_faction_id: int):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(
                        SystemMinorFactionDetails.system_id == system_id,
                        SystemMinorFactionDetails.minor_faction_id == minor_faction_id
                    )
                )
            )

            return result


    async def add(self, system_minor_faction_details: SystemMinorFactionDetails) -> bool:
        async with self.Session() as session:
            try:
                session.add(system_minor_faction_details)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def force_update(self, system_minor_faction_details: SystemMinorFactionDetails):
        async with self.Session() as session:
            try:
                await session.merge(system_minor_faction_details)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get(self, system_id: int, minor_faction_id: int):
        system_minor_faction_details: SystemMinorFactionDetails = None
        async with self.Session() as session:
            return await session.get(
                SystemMinorFactionDetails,
                (system_id, minor_faction_id)
            )


    async def delete(self, system_id: int, minor_faction_id: int):
        async with self.Session() as session:
            try:
                system_minor_faction_details = await session.get(
                    SystemMinorFactionDetails,
                    (system_id, minor_faction_id)
                )
                if system_minor_faction_details == None:
                    return False
                else:
                    await session.delete(system_minor_faction_details)
                    await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True

############################################

    async def set_influence(self, system_id: int, minor_faction_id: int, influence: float) -> bool:
        async with self.Session() as session:
            system_minor_faction_details = await session.get(
                SystemMinorFactionDetails,
                (system_id, minor_faction_id)
            )
            if system_minor_faction_details is None:
                return False

            system_minor_faction_details.influence = influence

            await session.commit()
            return True

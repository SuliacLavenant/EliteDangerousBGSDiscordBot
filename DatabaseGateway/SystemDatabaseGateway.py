import asyncio
import selectors
from sqlalchemy import func, select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.System import System


class SystemDatabaseGateway:
    def __init__(self, Session):
        self.Session = Session


    async def exists(self, system_name: str):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(System.name == system_name)
                )
            )

            return result


    async def add(self, system: System):
        async with self.Session() as session:
            try:
                session.add(system)
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                print(e.orig)
                return False

            return True


    async def force_update(self, system: System):
        async with self.Session() as session:
            try:
                await session.merge(system)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    # async def get(self, id: int):
    #     async with self.Session() as session:
    #         return await session.get(
    #             System,
    #             (id)
    #         )


    async def get_by_name(self, system_name: str, load_relation: bool = False):
        system: System = None
        async with self.Session() as session:
            result = await session.execute(
                select(System)
                .where(func.lower(System.name) == system_name.lower())
            )
            system = result.scalar_one_or_none()

            if system != None and load_relation:
                await session.refresh(system, ["system_minor_faction_details_dict"])

        return system


    async def get_all(self) -> list[System]:
        async with self.Session() as session:
            result = await session.scalars(select(System))
            return list(result.all())


    async def delete(self, system_name: str):
        return False # safety
        async with self.Session() as session:
            try:
                result = await session.execute(
                    select(System)
                    .where(System.name == system_name)
                )
                system = result.scalar_one_or_none()
                if system == None:
                    return False
                else:
                    await session.delete(system)
                    await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


############################################
    # check return TODO
    async def set_controlling_minor_faction_id(self, system_id: int, minor_faction_id: int) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.controlling_minor_faction_id = minor_faction_id

            await session.commit()        
            return True


    async def set_last_update_date_time(self, system_id: int, last_update: datetime) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.last_update = last_update

            await session.commit()        
            return True


    async def set_population(self, system_id: int, population: int) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.population = population

            await session.commit()        
            return True


    async def set_security(self, system_id: int, security: str) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.security = security

            await session.commit()        
            return True


    async def set_economy(self, system_id: int, economy: str) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.economy = economy

            await session.commit()        
            return True


    async def set_second_economy(self, system_id: int, second_economy: str) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.second_economy = second_economy

            await session.commit()        
            return True


    async def set_reserve(self, system_id: int, reserve: str) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.reserve = reserve

            await session.commit()        
            return True


    async def set_name(self, system_id: int, name: str) -> System | None:
        async with self.Session() as session:
            system = await session.get(
                System,
                (system_id)
            )
            if system is None:
                return False

            system.name = name

            await session.commit()        
            return True

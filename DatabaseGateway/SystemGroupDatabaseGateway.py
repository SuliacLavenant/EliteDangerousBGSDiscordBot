import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from DataClass.SystemGroup import SystemGroup


class SystemGroupDatabaseGateway:
    def __init__(self, Session):
        self.Session = Session


    async def exists(self, id: int):
        async with self.Session() as session:
            result = await session.scalar(
                select(
                    exists()
                    .where(
                        SystemGroup.id == id
                    )
                )
            )

            return result


    async def add(self, system_group: SystemGroup) -> bool:
        async with self.Session() as session:
            try:
                session.add(system_group)
                await session.commit()
            except IntegrityError as e:
                print(e)
                await session.rollback()
                return False

            return True


    async def force_update(self, system_group: SystemGroup):
        async with self.Session() as session:
            try:
                await session.merge(system_group)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


    async def get(self, id: int):
        async with self.Session() as session:
            return await session.get(
                SystemGroup,
                (id)
            )


    async def get_by_name(self, discord_id: int, system_group_name: str):
        system_group: SystemGroup = None
        async with self.Session() as session:
            result = await session.execute(
                select(SystemGroup)
                .where((SystemGroup.discord_id == discord_id) & (SystemGroup.name == system_group_name))
            )
            system_group = result.scalar_one_or_none()

        return system_group


    async def get_all_from_discord(self, discord_id: int) -> list[SystemGroup]:
        async with self.Session() as session:
            result = await session.scalars(
                select(SystemGroup)
                .where(SystemGroup.discord_id == discord_id)
            )

            return result.all()


    async def delete(self, id: int):
        async with self.Session() as session:
            try:
                system_group: SystemGroup = await session.get(
                    SystemGroup,
                    (id)
                )
                if system_group == None:
                    return False
                else:
                    await session.delete(system_group)
                    await session.commit()
            except IntegrityError:
                await session.rollback()
                return False

            return True


#####################################


    async def rename(self, id: int, new_name: str) -> bool:
        async with self.Session() as session:
            system_group: SystemGroup = await session.get(
                SystemGroup,
                (id)
            )
            if system_group is None:
                return False

            system_group.name = new_name

            await session.commit()
            return True


    async def set_color(self, id: int, color_rgb: list) -> bool:
        async with self.Session() as session:
            system_group: SystemGroup = await session.get(
                SystemGroup,
                (id)
            )
            if system_group is None:
                return False

            system_group.color_rgb = color_rgb

            await session.commit()
            return True

    async def set_emote(self, id: int, emote: str) -> bool:
        async with self.Session() as session:
            system_group: SystemGroup = await session.get(
                SystemGroup,
                (id)
            )
            if system_group is None:
                return False

            system_group.emote = emote

            await session.commit()
            return True

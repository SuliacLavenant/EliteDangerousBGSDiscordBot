import asyncio
import selectors
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from DatabaseGateway.DiscordTrackedSystemDatabaseGateway import DiscordTrackedSystemDatabaseGateway
from DatabaseGateway.GuildSettingsDatabaseGateway import GuildSettingsDatabaseGateway
from DatabaseGateway.MinorFactionDatabaseGateway import MinorFactionDatabaseGateway
from DatabaseGateway.PlayerDatabaseGateway import PlayerDatabaseGateway
from DatabaseGateway.SystemDatabaseGateway import SystemDatabaseGateway
from DatabaseGateway.SystemGroupDatabaseGateway import SystemGroupDatabaseGateway
from DatabaseGateway.SystemMinorFactionDetailsDatabaseGateway import SystemMinorFactionDetailsDatabaseGateway

class DatabaseGateway:

    @classmethod
    def setup(cls, user: str, password: str, port: int, database_name: str):
        DATABASE_URL = f"postgresql+psycopg://{user}:{password}@localhost:{str(port)}/{database_name}"
        engine = create_async_engine(DATABASE_URL)
        cls.Session = async_sessionmaker(engine, expire_on_commit=False)

        cls.discord_tracked_system = DiscordTrackedSystemDatabaseGateway(cls.Session)
        cls.guild_settings = GuildSettingsDatabaseGateway(cls.Session)
        cls.minor_faction = MinorFactionDatabaseGateway(cls.Session)
        cls.player = PlayerDatabaseGateway(cls.Session)
        cls.system = SystemDatabaseGateway(cls.Session)
        cls.system_group = SystemGroupDatabaseGateway(cls.Session)
        cls.system_minor_faction_details = SystemMinorFactionDetailsDatabaseGateway(cls.Session)

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.GuildSettings import GuildSettings
    from DataClass.System import System
    from DataClass.SystemGroup import SystemGroup

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class DiscordTrackedSystem(SQLAlchemyBase):
    __tablename__ = "discord_tracked_system"

    discord_id: Mapped[int] = mapped_column(ForeignKey("discord.id"), primary_key=True)
    guild_settings: Mapped["GuildSettings"] = relationship(back_populates="tracked_systems", lazy="selectin")

    system_id: Mapped[int] = mapped_column(ForeignKey("system.id"), primary_key=True)
    system: Mapped["System"] = relationship(back_populates="discord_trackings", lazy="selectin")

    system_group_id: Mapped[int] = mapped_column(ForeignKey("system_group.id"), nullable=True)
    system_group: Mapped["SystemGroup"] = relationship(back_populates="systems", lazy="selectin")

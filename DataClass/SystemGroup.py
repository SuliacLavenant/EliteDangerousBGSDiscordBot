from sqlalchemy import SmallInteger, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import ClassVar

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.DiscordTrackedSystem import DiscordTrackedSystem
    from DataClass.GuildSettings import GuildSettings

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class SystemGroup(SQLAlchemyBase):
    __tablename__ = "system_group"


    id: Mapped[int] = mapped_column(primary_key=True)

    discord_id: Mapped[int] = mapped_column(ForeignKey("discord.id"))
    guild_settings: Mapped["GuildSettings"] = relationship(back_populates="system_groups", lazy="raise")

    name: Mapped[str] = mapped_column(String)
    emote: Mapped[str] = mapped_column(String)

    color_rgb: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(SmallInteger)), default=lambda: [0,0,0], nullable=False)

    systems: Mapped[list["DiscordTrackedSystem"]] = relationship(back_populates="system_group", lazy="selectin")


    #not stored
    number_leader_systems: ClassVar[int] = None


    #TODO remove a lot of the following functions
    def haveSystem(self, system_name: str):
        return system_name.lower() in self.systems



    def calculate_number_leader_systems(self, system_recaps: dict):
        self.number_leader_systems = 0
        for system in self.systems:
            if system_recaps[system.system.name].is_leader:
                self.number_leader_systems += 1


    def __str__(self):
        return f"System Group Name: {self.name} | color: {self.rgb_color} | emote: {self.emote} | Systems: {self.systems}"

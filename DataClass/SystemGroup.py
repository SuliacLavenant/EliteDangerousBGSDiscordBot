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
    def rename(self, name: str):
        self.name = name


    def set_rgb_color(self, rgb_color: tuple):
        self.rgb_color = rgb_color


    def haveSystem(self, system_name: str):
        return system_name.lower() in self.systems


    def addSystem(self, system_name: str):
        self.systems.append(system_name.lower())


    def add_systems(self, system_name_list: list):
        for system_name in system_name_list:
            self.addSystem(system_name)


    def removeSystem(self, system_name: str):
        if system_name in self.systems:
            self.systems.remove(system_name)
            return True
        else:
            return False


    def remove_systems(self, system_name_list: str):
        removed = True
        for system_name in system_name_list:
            removed = removed and self.removeSystem(system_name)
        return removed


    def get_as_dict(self) -> dict:
        system_group_dict = {}
        system_group_dict["name"] = self.name
        system_group_dict["rgb_color"] = self.rgb_color
        system_group_dict["emote"] = self.emote
        system_group_dict["systems"] = self.systems

        return system_group_dict


    def calculate_number_leader_systems(self, system_recaps: dict):
        self.number_leader_systems = 0
        for system in self.systems:
            if system_recaps[system.system.name].is_leader:
                self.number_leader_systems += 1


    def __str__(self):
        return f"System Group Name: {self.name} | color: {self.rgb_color} | emote: {self.emote} | Systems: {self.systems}"

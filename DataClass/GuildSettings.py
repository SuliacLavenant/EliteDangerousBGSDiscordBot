from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.DiscordTrackedSystem import DiscordTrackedSystem
    from DataClass.MinorFaction import MinorFaction
    from DataClass.SystemGroup import SystemGroup

from DataClass.SQLAlchemyBase import SQLAlchemyBase


# WARNING take care diffrence discord id (id) and guild id
class GuildSettings(SQLAlchemyBase):
    __tablename__ = "discord"


    id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    minor_faction_id: Mapped[int | None] = mapped_column(ForeignKey("minor_faction.id"), nullable=True)
    minor_faction: Mapped["MinorFaction | None"] = relationship(lazy="selectin")

    #squadron_id: int = None

    # OLD
    display_untracked_systems_in_recap: bool = True

    #channels
    bgs_change_log_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    bgs_system_recap_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    bgs_warning_recap_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mission_recap_channel_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    trusted_channel_ids: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(BigInteger)), default=list, nullable=False)


    tracked_systems: Mapped[list["DiscordTrackedSystem"]] = relationship(back_populates="guild_settings", lazy="raise")

    system_groups: Mapped[list["SystemGroup"]] = relationship(back_populates="guild_settings", lazy="raise")


    def is_channel_trusted(self, channel_id: int) -> bool:
        return channel_id in self.trusted_channel_ids


    def get_tracked_system_with_no_group(self):
        tracked_system_without_group: list = []
        for tracked_system in self.tracked_systems:
            if tracked_system.system_group_id is None:
                tracked_system_without_group.append(tracked_system)
        #TODO add sort
        return tracked_system_without_group


    def get_tracked_system_names_with_no_group(self):
        tracked_system_names_with_no_group: list = []
        for tracked_system in self.tracked_systems:
            if tracked_system.system_group_id is None:
                tracked_system_names_with_no_group.append(tracked_system.system.name)
        tracked_system_names_with_no_group.sort()
        return tracked_system_names_with_no_group

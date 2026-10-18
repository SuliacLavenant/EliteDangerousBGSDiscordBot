from sqlalchemy import ForeignKey, REAL, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.MinorFaction import MinorFaction
    from DataClass.System import System

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class SystemMinorFactionDetails(SQLAlchemyBase):
    __tablename__ = "system_minor_faction_details"

    system_id: Mapped[int] = mapped_column(ForeignKey("system.id"), primary_key=True)
    system: Mapped["System"] = relationship(back_populates="system_minor_faction_details_dict", lazy="selectin")

    minor_faction_id: Mapped[int] = mapped_column(ForeignKey("minor_faction.id"), primary_key=True)
    minor_faction: Mapped["MinorFaction"] = relationship(back_populates="system_minor_faction_details_list", lazy="selectin")

    influence: Mapped[float | None] = mapped_column(REAL)

    pending_states: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    active_states: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    recovering_states: Mapped[list[str] | None] = mapped_column(ARRAY(String))

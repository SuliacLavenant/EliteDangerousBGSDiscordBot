from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.SystemMinorFactionDetails import SystemMinorFactionDetails

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class MinorFaction(SQLAlchemyBase):
    __tablename__ = "minor_faction"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, unique=True)
    allegiance: Mapped[str | None] = mapped_column(String, nullable=True)
    government: Mapped[str | None] = mapped_column(String, nullable=True)

    origin_system_id: Mapped[int | None] = mapped_column(ForeignKey("system.id"), nullable=True)
    origin_system: Mapped[System | None] = relationship(foreign_keys=[origin_system_id], lazy="raise")

    system_minor_faction_details_list: Mapped[list["SystemMinorFactionDetails"]] = relationship(back_populates="minor_faction", lazy="raise")

##################################################
################################################## systems

    # def get_shared_system_names(self, minor_faction):
    #     shared_system_names = []
    #     for system_name in self.system_names:
    #         if system_name in minor_faction.system_names:
    #             shared_system_names.append(system_name)
    #     return shared_system_names


############################################################################################
###################################### STR Functions #######################################
############################################################################################

    def __str__(self):
        return f"Minor Faction: {self.name.title()} | Allegiance: {self.allegiance} | Government: {self.government}"# | Origin System: {self.origin_system_name.title()} | present in {len(self.system_names)} common systems"


    def get_allegiance_str(self) -> str:
        if self.allegiance != None:
            return self.allegiance.title()
        else:
            return "??"


    def get_government_str(self) -> str:
        if self.government != None:
            return self.government.title()
        else:
            return "??"

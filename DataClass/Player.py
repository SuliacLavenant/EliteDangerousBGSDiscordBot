from sqlalchemy import BigInteger, Boolean, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class Player(SQLAlchemyBase):
    __tablename__ = "player"


    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column(Integer, nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    inara_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    discord_account_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)


    other_names: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), default=list, nullable=False)



    #alternative_account_ids: list[int] = field(default_factory=list[int])
    #architected_systems: list[str]
    #note: str = None
    #squadron_id: int = None





##################################################
################################################## architected system

    def add_architected_system(self, system_name: str) -> bool:
        if system_name.lower() not in self.architected_systems:
            self.architected_systems.append(system_name.lower())
            self.architected_systems.sort()
            return True
        else:
            return False


    def remove_architected_system(self, system_name: str) -> bool:
        if system_name.lower() in self.architected_systems:
            self.architected_systems.remove(system_name.lower())
            self.architected_systems.sort()
            return True
        else:
            return False


##################################################
################################################## other names

    def add_other_name(self, other_name: str) -> bool:
        if other_name not in self.other_names:
            self.other_names.append(other_name)
            return True
        else:
            return False


##################################################
################################################## str

    def __str__(self):
        return f"Name: {self.name.title()}"

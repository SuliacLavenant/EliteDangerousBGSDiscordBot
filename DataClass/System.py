from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from typing import ClassVar



import asyncio



from copy import deepcopy
import urllib.parse

# from DataClass.MinorFaction import MinorFaction
from EventClass.SystemEvent.SystemEvent import SystemEvent
from EventClass.SystemEvent.ConflictEndSystemEvent import ConflictEndSystemEvent
from EventClass.SystemEvent.ConflictStartSystemEvent import ConflictStartSystemEvent
from EventClass.SystemEvent.MinorFactionAcquireLeadershipSystemEvent import MinorFactionAcquireLeadershipSystemEvent
from EventClass.SystemEvent.MinorFactionJoinSystemEvent import MinorFactionJoinSystemEvent
from EventClass.SystemEvent.MinorFactionLeaveSystemEvent import MinorFactionLeaveSystemEvent
from EventClass.SystemEvent.MinorFactionLoseLeadershipSystemEvent import MinorFactionLoseLeadershipSystemEvent
#from EventClass.SystemEvent import 


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataClass.DiscordTrackedSystem import DiscordTrackedSystem
    from DataClass.SystemMinorFactionDetails import SystemMinorFactionDetails

from DataClass.SQLAlchemyBase import SQLAlchemyBase


class System(SQLAlchemyBase):
    __tablename__ = "system"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, unique=True)
    population: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    security: Mapped[str | None] = mapped_column(String, nullable=True)
    economy: Mapped[str | None] = mapped_column(String, nullable=True)
    second_economy: Mapped[str | None] = mapped_column(String, nullable=True)
    reserve: Mapped[str | None] = mapped_column(String, nullable=True)

    is_architected: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    architect_name: Mapped[str | None] = mapped_column(String, nullable=True)

    last_update: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)

    controlling_faction_name: ClassVar[str | None] = None #used for some api
    controlling_minor_faction_id: Mapped[int | None] = mapped_column(ForeignKey("minor_faction.id"), nullable=True)
    # controlling_minor_faction: MinorFaction = None

    system_minor_faction_details_dict: Mapped[dict[int, "SystemMinorFactionDetails"]] = relationship(back_populates="system", collection_class=attribute_keyed_dict("minor_faction_id"), lazy="selectin")


    discord_trackings: Mapped[list["DiscordTrackedSystem"]] = relationship(back_populates="system", lazy="raise")


    is_stored: bool = True #TODO for tmp class set it to false #TODO to juste remove

############################################################################################
############################################################################################

    #TODO confirm methods with a #
    def is_controlled_by(self, minor_faction: MinorFaction) -> bool:
        return self.controlling_minor_faction_id == minor_faction.id


    def minor_faction_is_present(self, minor_faction_name: str):#
        return minor_faction_name.lower() in self.minor_factions_names


    def get_minor_faction_position(self, minor_faction: MinorFaction) -> int:
        if self.is_controlled_by(minor_faction):
            return 1

        influence: int = -1
        if minor_faction.id in self.system_minor_faction_details_dict:
            influence = self.system_minor_faction_details_dict[minor_faction.id].influence

        if influence == -1:
            return -1
        else:
            position = 1
            for system_minor_faction_details in self.system_minor_faction_details_dict.values():
                if system_minor_faction_details.minor_faction_id != minor_faction.id:
                    if influence < system_minor_faction_details.influence:
                        position+=1
            
            return position


    def get_minor_factions_ranking(self) -> dict:
        ranking = {}
        for system_minor_faction_details in self.system_minor_faction_details_dict.values():
            rank = self.get_minor_faction_position(system_minor_faction_details.minor_faction)
            if rank in ranking.keys():
                ranking[rank+1] = system_minor_faction_details.minor_faction_id
            else:
                ranking[rank] = system_minor_faction_details.minor_faction_id

        return ranking


    def get_leader_influence(self) -> float:
        return self.system_minor_faction_details_dict[self.controlling_minor_faction_id].influence


    def get_leader_influence_margin(self) -> float:
        leader_influence: float = self.get_leader_influence()
        second_influence: float = 0

        for system_minor_faction_details in self.system_minor_faction_details_dict.values():
            if system_minor_faction_details.minor_faction_id != self.controlling_minor_faction_id:
                faction_influence: float = system_minor_faction_details.influence
                if faction_influence > second_influence:
                    second_influence = faction_influence

        return leader_influence-second_influence


    def get_minor_faction_influence_difference_from_leader(self, minor_faction_name: str) -> float:#
        return self.get_minor_faction_influence(minor_faction_name.lower()) - self.get_leader_influence()


    def get_second_and_its_influence(self):#
        second = ""
        second_influence = 0

        for minor_faction_name in self.minor_factions_names:
            if minor_faction_name!=self.controlling_faction_name:
                faction_influence = self.minor_factions_influence[minor_faction_name]
                if faction_influence>second_influence:
                    second_influence = faction_influence
                    second = minor_faction_name

        return (second,second_influence)


    def get_minor_faction_influence(self, minor_faction: MinorFaction) -> float:
        if minor_faction.id in self.system_minor_faction_details_dict:
            return self.system_minor_faction_details_dict[minor_faction.id].influence
        else:
            return 0


    def do_minor_faction_have_state(self, minor_faction: str, state: str) -> str:#
        system_minor_faction_details: SystemMinorFactionDetails = self.system_minor_faction_details_dict[minor_faction.id]
        if system_minor_faction_details.pending_states is not None and state in system_minor_faction_details.pending_states:
            return "pending"
        if system_minor_faction_details.active_states is not None and state in system_minor_faction_details.active_states:
            return "active"
        if system_minor_faction_details.recovering_states is not None and state in system_minor_faction_details.recovering_states:
            return "recovering"
        else:
            return None


    def get_minor_faction_conflict_state(self, minor_faction: MinorFaction) -> str:
        if self.do_minor_faction_have_the_same_influence_as_another(minor_faction):
            war = self.do_minor_faction_have_state(minor_faction, "war")
            if war == "pending" or war == "active":
                return "war"
            civilWar = self.do_minor_faction_have_state(minor_faction, "civil war")
            if civilWar == "pending" or civilWar == "active":
                return "civil war"
            election = self.do_minor_faction_have_state(minor_faction, "election")
            if election == "pending" or election == "active":
                return "election"
        return None


    def do_minor_faction_have_the_same_influence_as_another(self, minor_faction: MinorFaction) -> bool:
        minor_faction_influence: float = self.system_minor_faction_details_dict[minor_faction.id].influence

        for system_minor_faction_details in self.system_minor_faction_details_dict.values():
            if system_minor_faction_details.minor_faction_id != minor_faction.id:
                if system_minor_faction_details.influence == minor_faction_influence:
                    return True
        return False


    def add_mission(self, mission_id: int):#
        self.mission_ids.append(mission_id)


    def remove_mission(self, mission_id: int):#
        self.mission_ids.remove(mission_id)


    def lower(self, string: str):#
        return string.lower() if isinstance(string, str) else string


############################################################################################
###################################### STR Functions #######################################
############################################################################################

    def __str__(self):
        return f"System: {self.name.title()} | Population: {self.population} | controlling_minor_faction_id: {self.controlling_minor_faction_id}"


    def get_economy_str(self) -> str:
        if self.economy == None:
            return "??"
        elif self.second_economy == None:
            return self.economy.title()
        else:
            return f"{self.economy.title()} / {self.second_economy.title()}"


    def get_population_str(self) -> str:
        if self.population == -1:
            return "??"
        match len(str(self.population)):
            case 0 | 1 | 2 | 3:
                return str(self.population)
            case 4 | 5 | 6:
                return f"{str(self.population)[:3]},{str(self.population)[3:]}"
            case 7 | 8 | 9:
                return f"{str(round(self.population/1000000,2))} million"
            case _:
                return f"{str(round(self.population/1000000000,2))} billion"


    def get_security_str(self) -> str:
        if self.security == None:
            return "??"
        else:
            return self.security.title()


    def get_system_name_with_inara_link(self) -> str:
        return f"[**{self.name}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.name.lower())})"

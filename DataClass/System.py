from dataclasses import dataclass, field
from copy import deepcopy

from DataClass.MinorFaction import MinorFaction
from EventClass.SystemEvent.SystemEvent import SystemEvent
from EventClass.SystemEvent.ConflictEndSystemEvent import ConflictEndSystemEvent
from EventClass.SystemEvent.ConflictStartSystemEvent import ConflictStartSystemEvent
from EventClass.SystemEvent.MinorFactionJoinSystemEvent import MinorFactionJoinSystemEvent
from EventClass.SystemEvent.MinorFactionLeaveSystemEvent import MinorFactionLeaveSystemEvent
#from EventClass.SystemEvent import 

@dataclass
class System:
    name: str = ""
    population: int = -1
    security: str = ""
    economy: str = ""
    second_economy: str = ""
    reserve: str = ""

    controlling_faction_name: str = ""

    minor_factions_names: list[str] = field(default_factory=list)
    minor_factions: dict[str,MinorFaction] = field(default_factory=dict)
    minor_factions_influence: dict[str, int] = field(default_factory=dict)
    minor_factions_states: dict[str, dict] = field(default_factory=dict)

    isOrigin: bool = False
    isArchitected: bool = None
    architect: str = ""
    isDiplomatic: bool = False

    lastInfluenceUpdate: int = 0 #unix time

    isStored: int = False #stored system


    @classmethod
    def init_from_dict(cls, system_dict: dict):
        system = cls(
            name = system_dict["name"],
            population = system_dict["population"],
            security = system_dict["security"],
            economy = system_dict["economy"],
            second_economy = system_dict["second_economy"],
            reserve = system_dict["reserve"],
            controlling_faction_name = system_dict["controlling_faction_name"],
            minor_factions_names = system_dict["minor_factions_names"],
            minor_factions_influence = system_dict["minor_factions_influence"],
            minor_factions_states = system_dict["minor_factions_states"],
            isOrigin = system_dict["isOrigin"],
            isArchitected = system_dict["isArchitected"],
            architect = system_dict["architect"],
            isDiplomatic = system_dict["isDiplomatic"],
            lastInfluenceUpdate = system_dict["lastInfluenceUpdate"],
            isStored = True
            )
        return system


    def __post_init__(self):
        self.name = self.name.lower()
        self.security = self.security.lower()
        self.economy = self.economy.lower()
        self.second_economy = self.second_economy.lower() if self.second_economy!=None else None
        self.reserve = self.reserve.lower() if self.reserve!=None else None
        self.controlling_faction_name = self.controlling_faction_name.lower()
        self.architect = self.architect.lower()


    def get_as_dict(self) -> dict:
        system_dict = {}
        system_dict["name"] = self.name
        system_dict["population"] = self.population
        system_dict["security"] = self.security
        system_dict["economy"] = self.economy
        system_dict["second_economy"] = self.second_economy
        system_dict["reserve"] = self.reserve
        system_dict["controlling_faction_name"] = self.controlling_faction_name
        system_dict["minor_factions_names"] = self.minor_factions_names
        system_dict["minor_factions_influence"] = self.minor_factions_influence
        system_dict["minor_factions_states"] = self.minor_factions_states
        system_dict["isOrigin"] = self.isOrigin
        system_dict["isArchitected"] = self.isArchitected
        system_dict["architect"] = self.architect
        system_dict["isDiplomatic"] = self.isDiplomatic
        system_dict["lastInfluenceUpdate"] = self.lastInfluenceUpdate

        return system_dict


    def add_faction(self, name: str, allegiance: str, government: str, influence: int, pendingStates: list, activeStates: list, recoveringStates: list):
        self.minor_factions[name.lower()] = MinorFaction(name=name,allegiance=allegiance,government=government)
        self.minor_factions_names.append(name.lower())
        self.minor_factions_influence[name.lower()] = influence
        self.minor_factions_states[name.lower()] = {"pendingStates": pendingStates, "activeStates": activeStates, "recoveringStates": recoveringStates}


    def diff(self, system_new):
        system_events = []
        if system_new!=None:
            # faction join
            for minor_faction_name in system_new.minor_factions_names:
                if minor_faction_name not in self.minor_factions_names:
                    system_events.append(MinorFactionJoinSystemEvent(minor_faction_name=minor_faction_name,system_name=self.name))
            # faction leave
            for minor_faction_name in self.minor_factions_names:
                if minor_faction_name not in system_new.minor_factions_names:
                    system_events.append(MinorFactionLeaveSystemEvent(minor_faction_name=minor_faction_name,system_name=self.name))
        
        return system_events


    def update(self, system_new):
        if system_new!=None:
            self.population = system_new.population
            self.security = system_new.security
            self.economy = system_new.economy
            self.second_economy = system_new.second_economy
            self.controlling_faction_name = system_new.controlling_faction_name

            self.minor_factions = system_new.minor_factions
            self.minor_factions_names = system_new.minor_factions_names
            self.minor_factions_influence = system_new.minor_factions_influence
            self.minor_factions_states = system_new.minor_factions_states

            self.lastInfluenceUpdate = system_new.lastInfluenceUpdate


    ### Method
    def is_controlled_by(self, minor_faction_name: str):
        return self.controlling_faction_name == minor_faction_name.lower()


    def minor_faction_is_present(self, minor_faction_name: str):
        return minor_faction_name.lower() in self.minor_factions_names


    def get_minor_faction_position(self, minor_faction_name: str) -> int:
        if minor_faction_name not in self.minor_factions_names:
            return -1
        elif self.is_controlled_by(minor_faction_name):
            return 1
        else:
            position = 1
            influence = self.minor_factions_influence[minor_faction_name]
            for minor_faction_name_2 in self.minor_factions_names:
                if minor_faction_name_2!=minor_faction_name:
                    if influence < self.minor_factions_influence[minor_faction_name_2]:
                        position+=1
            return position


    def get_minor_factions_ranking(self):
        ranking = {}
        for minor_faction_name in self.minor_factions_names:
            rank = self.get_minor_faction_position(minor_faction_name)
            if rank in ranking.keys():
                ranking[rank+1] = minor_faction_name
            else:
                ranking[rank] = minor_faction_name
        return ranking


    def get_leader_influence(self):
        return self.minor_factions_influence[self.controlling_faction_name]


    def get_leader_influence_margin(self):
        leader_influence = self.get_leader_influence()
        second_influence = 0

        for minor_faction_name in self.minor_factions_names:
            if minor_faction_name!=self.controlling_faction_name:
                faction_influence = self.minor_factions_influence[minor_faction_name]
                if faction_influence>second_influence:
                    second_influence = faction_influence

        return leader_influence-second_influence
    

    def get_minor_faction_influence_difference_from_leader(self, minor_faction_name: str) -> float:
        return self.get_minor_faction_influence(minor_faction_name) - self.get_leader_influence()


    def get_second_and_its_influence(self):
        second = ""
        second_influence = 0

        for minor_faction_name in self.minor_factions_names:
            if minor_faction_name!=self.controlling_faction_name:
                faction_influence = self.minor_factions_influence[minor_faction_name]
                if faction_influence>second_influence:
                    second_influence = faction_influence
                    second = minor_faction_name

        return (second,second_influence)


    def get_minor_faction_influence(self, minor_faction_name: str):
        if minor_faction_name in self.minor_factions_names:
            return self.minor_factions_influence[minor_faction_name]
        else:
            return 0


    def do_minor_faction_have_state(self, minor_faction_name: str, state: str):
        if state in self.minor_factions_states[minor_faction_name]["pendingStates"]:
            return "pending"
        elif state in self.minor_factions_states[minor_faction_name]["activeStates"]:
            return "active"
        elif state in self.minor_factions_states[minor_faction_name]["recoveringStates"]:
            return "recovering"
        else:
            return None
        
    def get_minor_faction_conflict_state(self, minor_faction_name: str):
        if self.do_minor_faction_have_the_same_influence_as_another(minor_faction_name):
            war = self.do_minor_faction_have_state(minor_faction_name, "war")
            if war == "pending" or war == "active":
                return "war"
            civilWar = self.do_minor_faction_have_state(minor_faction_name, "civil war")
            if civilWar == "pending" or civilWar == "active":
                return "civil war"
            election = self.do_minor_faction_have_state(minor_faction_name, "election")
            if election == "pending" or election == "active":
                return "election"
        return None
    
    def do_minor_faction_have_the_same_influence_as_another(self, minor_faction_name: str):
        minor_faction_influence = self.minor_factions_influence[minor_faction_name]
        for minor_faction_name_2 in self.minor_factions_names:
            if minor_faction_name_2 != minor_faction_name:
                faction_influence = self.minor_factions_influence[minor_faction_name_2]
                if faction_influence == minor_faction_influence:
                    return True
        return False


    def lower(self, string: str):
        return string.lower() if isinstance(string, str) else string




##########################################################################################################
###################################### STR Functions #####################################################
##########################################################################################################

    def getStrSystemEconomy(self):
        if self.second_economy == None:
            return self.economy.title()
        else:
            return f"{self.economy.title()} / {self.second_economy.title()}"
        
    def getStrSystemPopulation(self):
        if self.population == -1:
            return "?"
        match len(str(self.population)):
            case 0 | 1 | 2 | 3:
                return str(self.population)
            case 4 | 5 | 6:
                return f"{str(self.population)[:3]},{str(self.population)[3:]}"
            case 7 | 8 | 9:
                return f"{str(round(self.population/1000000,2))} million"
            case _:
                return f"{str(round(self.population/1000000000,2))} billion"

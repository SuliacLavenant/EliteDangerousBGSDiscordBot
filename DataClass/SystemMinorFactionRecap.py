from dataclasses import dataclass, field
from copy import deepcopy
from datetime import datetime, timezone

from BotConfig.BotConfig import BotConfig
from DataClass.System import System
# from DataClass.DiplomaticSystem import DiplomaticSystem
from DataClass.SystemGroup import SystemGroup
from DataClass.MinorFaction import MinorFaction

@dataclass
class SystemMinorFactionRecap:
    system: System
    influence: int = -1
    is_leader: bool = None
    leader_influence_margin: int = None
    influence_warning_level: int = -1
    isArchitect: bool = None
    leader_influence: int = -1

    expansion_warning: bool = False
    retreat: bool = False
    retreat_warning: bool = False

    warning: str = None
    important_state: str = None
    position_in_system: str = None
    # numberOfFactions: int = 0

    margin_warning: bool = False

    days_since_last_update: int = -1

    isOrigin: bool = False
    isArchitect: bool = False

    is_diplomatic: bool = False
    diplomaticWarning: str = None

    in_conflict: bool = False


    system_group: SystemGroup = None

    def __init__(self, system: System, minor_faction: MinorFaction, diplomaticSystem: DiplomaticSystem = None, system_group: SystemGroup = None):
        self.system = system
        self.minor_faction = minor_faction
        self.system_group = system_group
        
        self.diplomaticSystem = diplomaticSystem
        self.is_diplomatic = self.diplomaticSystem is not None

        self.influence = self.system.get_minor_faction_influence(self.minor_faction)
        self.leader_influence = system.get_leader_influence()
        self.is_leader = system.is_controlled_by(self.minor_faction)

        if self.influence != 0:
            if self.is_leader:
                self.leader_influence_margin = self.system.get_leader_influence_margin()
                #self.calculate_leader_influence_margin_warning() # not needed, caculated in check_influence_warning

            self.check_retreat_warning()
            self.check_expansion_warning()
            self.check_important_state()

            self.check_position_in_system() #TODO maybe move the is_leader in this
            self.check_influence_warning()

            # self.checkDiplomaticPosition()
        else:
            print("not in system")

        self.number_of_factions = len(self.system.system_minor_faction_details_dict)
        self.calculate_days_since_last_update()


    #Calculate influence warning
    def check_influence_warning(self):
        if self.expansion_warning:
            self.warning = "expansion"
        elif self.is_leader:
            self.warning = self.calculate_leader_influence_margin_warning()
        elif self.retreat_warning:
            self.warning = "retreat"
        elif self.important_state != None:
            self.warning = "important"


    def calculate_leader_influence_margin_warning(self):
        if self.leader_influence_margin < BotConfig.bgs.leader_influence_warning.level3:
            self.margin_warning = True
            self.influence_warning_level = 3
            return "marginLvl3"
        elif self.leader_influence_margin < BotConfig.bgs.leader_influence_warning.level2:
            self.margin_warning = True
            self.influence_warning_level = 2
            return "marginLvl2"
        elif self.leader_influence_margin < BotConfig.bgs.leader_influence_warning.level1:
            self.margin_warning = True
            self.influence_warning_level = 1
            return "marginLvl1"
        else:
            self.influence_warning_level = 0
            return "marginLvl0"


    def check_expansion_warning(self):
        self.expansion_warning = self.system.get_minor_faction_influence(self.minor_faction) >= BotConfig.bgs.state.expansion.warning_influence


    def check_retreat_warning(self):
        self.retreat = self.system.do_minor_faction_have_state(self.minor_faction, "retreat") != None
        self.retreat_warning = self.system.get_minor_faction_influence(self.minor_faction) <= BotConfig.bgs.state.retreat.warning_influence or self.retreat


    def check_important_state(self):
        if self.retreat:
            self.important_state = "retreat"
        conflict_state = self.system.get_minor_faction_conflict_state(self.minor_faction)
        if conflict_state is not None:
            self.in_conflict = True
            self.important_state = conflict_state


    def check_position_in_system(self):
        if self.is_leader:
            self.position_in_system = "leader"
        elif self.is_diplomatic:
            self.position_in_system = "diplomatic"
        else:
            self.position_in_system = "other"


    def checkDiplomaticPosition(self):#
        if self.system.is_diplomatic:
            if self.minorFactionName in self.diplomaticSystem.diplomaticPositions.keys():
                minorFactionPosition = self.system.get_minor_faction_position(self.minorFactionName)
                match self.diplomaticSystem.diplomaticPositions[self.minorFactionName]:
                    case 1:
                        if minorFactionPosition != 1:
                            self.diplomaticWarning = "shouldBeLeader"
                    case 2:
                        if minorFactionPosition == 1:
                            self.diplomaticWarning = "shouldNotBeLeader"
                        elif minorFactionPosition == 2:
                            self.diplomaticWarning = "notLeaderGood"
                        else:
                            self.diplomaticWarning = "shouldtBeSecond"
                    case _:
                        for otherMinoFactionName in self.diplomaticSystem.diplomaticPositions.keys():
                            if self.diplomaticSystem.diplomaticPositions[otherMinoFactionName] == 1:
                                if self.system.get_minor_faction_position(otherMinoFactionName) != 1 and minorFactionPosition == 1:
                                    self.diplomaticWarning = "shouldNotBeLeader"
                                else:
                                    self.diplomaticWarning = "notLeaderGood"


    def calculate_days_since_last_update(self):
        if self.system.last_update != None:
            time_since_last_update = datetime.now(timezone.utc) - self.system.last_update
            self.days_since_last_update = time_since_last_update.days
        else:
            self.days_since_last_update = None


    def __str__(self):#
        if self.is_leader:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | leader, influence warning level {self.influence_warning_level} ({round(self.leader_influence_margin*100, 2)}% margin) | architect {self.isArchitect}"
        else:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | architect {self.isArchitect}"

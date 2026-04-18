from dataclasses import dataclass, field

from BotConfig.BotConfig import BotConfig
from DataClass.Mission.MissionProgressEnum import MissionProgressEnum
from DataClass.Mission.SystemMission.SystemMission import SystemMission
from DataClass.System import System

@dataclass
class SetMinorFactionAsLeaderInSystemMission(SystemMission):
    minor_faction_name: str = None
    mission_id: int = None
    mission_type: str = "SetMinorFactionAsLeaderInSystemMission"
    system_name: str = None

    #not stored
    current_influence_difference: float = None
    conflict: str = None
    state = MissionProgressEnum.NONE
    system: System = None


    @classmethod
    def init_from_dict(cls, mission_dict: dict):
        system_mission = cls(
            minor_faction_name=mission_dict["minor_faction_name"],
            mission_id=mission_dict["mission_id"],
            mission_type=mission_dict["mission_type"],
            system_name=mission_dict["system_name"]
            )
        return system_mission


    def get_as_dict(self) -> dict:
        mission_dict = {}
        mission_dict["minor_faction_name"] = self.minor_faction_name
        mission_dict["mission_id"] = self.mission_id
        mission_dict["mission_type"] = self.mission_type
        mission_dict["system_name"] = self.system_name
        return mission_dict


    def update_with_system_data(self, system: System):
        self.system = system

        if self.system.is_controlled_by(self.minor_faction_name):
            self.current_influence_difference = self.system.get_leader_influence_margin()
        else:
            self.current_influence_difference = self.system.get_minor_faction_influence_difference_from_leader(self.minor_faction_name)

        self.conflict = self.system.get_minor_faction_conflict_state(self.minor_faction_name)

    def check_mission_state(self):
        if self.system.is_controlled_by(self.minor_faction_name) and self.conflict == None:
            self.state = MissionProgressEnum.COMPLETE
        else:
            self.state = MissionProgressEnum.ACTIVE

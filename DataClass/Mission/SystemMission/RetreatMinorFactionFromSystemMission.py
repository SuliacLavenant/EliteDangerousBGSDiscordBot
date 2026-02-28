from dataclasses import dataclass, field

from BotConfig.BotConfig import BotConfig
from DataClass.Mission.MissionProgressEnum import MissionProgressEnum
from DataClass.Mission.SystemMission.SystemMission import SystemMission
from DataClass.System import System

@dataclass
class RetreatMinorFactionFromSystemMission(SystemMission):
    minor_faction_name: str = None
    mission_id: int = None
    mission_type: str = "RetreatMinorFactionFromSystemMission"
    system_name: str = None

    #not stored
    current_influence: int = None
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
        self.current_influence = self.system.get_minor_faction_influence(self.minor_faction_name)


    def check_mission_state(self):
        if self.current_influence == 0:
            self.state = MissionProgressEnum.COMPLETE
        elif self.current_influence <= BotConfig.bgs.state.retreat.trigger_influence:
            self.state = MissionProgressEnum.PENDING
        else:
            self.state = MissionProgressEnum.IN_PROGRESS

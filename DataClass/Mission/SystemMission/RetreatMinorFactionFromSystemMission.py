from dataclasses import dataclass, field

from DataClass.Mission.SystemMission.SystemMission import SystemMission

@dataclass
class RetreatMinorFactionFromSystemMission(SystemMission):
    minor_faction_name: str = None
    mission_id: int = None
    mission_type: str = "RetreatMinorFactionFromSystemMission"
    system_name: str = None


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

from dataclasses import dataclass, field

from DataClass.Mission.MissionProgressEnum import MissionProgressEnum

@dataclass
class Mission:
    mission_id: int = None
    mission_type: str = None

    #not stored
    state = MissionProgressEnum.NONE

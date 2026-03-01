from enum import Enum

class MissionProgressEnum(Enum):
    NONE = "none"

    UPCOMING = "upcoming"
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETE = "complete"

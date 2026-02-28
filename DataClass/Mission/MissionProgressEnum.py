from enum import Enum

class MissionProgressEnum(Enum):
    NONE = "none"

    UPCOMING = "upcoming"
    NOT_ASSIGNED = "not_assigned"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    COMPLETE = "complete"

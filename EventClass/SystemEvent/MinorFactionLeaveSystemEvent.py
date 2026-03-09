from dataclasses import dataclass, field

from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

@dataclass
class MinorFactionLeaveSystemEvent(MinorFactionSystemEvent):
    event_type: str = "MinorFactionLeaveSystemEvent" 
    minor_faction_name: str = None
    system_name: str = None

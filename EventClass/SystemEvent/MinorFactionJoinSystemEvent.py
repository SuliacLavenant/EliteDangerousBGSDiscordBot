from dataclasses import dataclass, field

from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

@dataclass
class MinorFactionJoinSystemEvent(MinorFactionSystemEvent):
    event_type: str = "MinorFactionJoinSystemEvent" 
    minor_faction_name: str = None
    system_name: str = None

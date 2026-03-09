from dataclasses import dataclass, field

from EventClass.SystemEvent.SystemEvent import SystemEvent

@dataclass
class MinorFactionSystemEvent(SystemEvent):
    event_type: str = "MinorFactionSystemEvent" 
    minor_faction_name: str = None
    system_name: str = None

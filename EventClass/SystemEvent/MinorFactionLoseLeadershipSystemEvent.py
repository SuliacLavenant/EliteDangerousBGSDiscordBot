from dataclasses import dataclass, field

from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

@dataclass
class MinorFactionLoseLeadershipSystemEvent(MinorFactionSystemEvent):
    event_type: str = "MinorFactionLoseLeadershipSystemEvent" 
    minor_faction_name: str = None
    new_leader_minor_faction_name: str = None
    system_name: str = None

from dataclasses import dataclass, field

from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

@dataclass
class MinorFactionAcquireLeadershipSystemEvent(MinorFactionSystemEvent):
    event_type: str = "MinorFactionAcquireLeadershipSystemEvent" 
    minor_faction_name: str = None
    old_leader_minor_faction_name: str = None
    system_name: str = None

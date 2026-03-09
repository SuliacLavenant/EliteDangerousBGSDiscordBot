from dataclasses import dataclass, field

from EventClass.SystemEvent.SystemEvent import SystemEvent

@dataclass
class ConflictSystemEvent(SystemEvent):
    conflict: str = None # war or election
    event_type: str = "ConflictSystemEvent" 
    minor_faction_names: tuple = field(default_factory=tuple) # (minor_faction_1_name, minor_faction_2_name)
    system_name: str = None

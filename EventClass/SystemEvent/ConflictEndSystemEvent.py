from dataclasses import dataclass, field

from EventClass.SystemEvent.ConflictSystemEvent import ConflictSystemEvent

@dataclass
class ConflictEndSystemEvent(ConflictSystemEvent):
    conflict: str = None # war or election
    event_type: str = "ConflictEndSystemEvent" 
    minor_faction_names: tuple = field(default_factory=tuple) # (minor_faction_1_name, minor_faction_2_name)
    system_name: str = None
    winner: int = None # None, 0, 1 

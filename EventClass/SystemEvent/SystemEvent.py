from dataclasses import dataclass, field

@dataclass
class SystemEvent:
    event_type: str = "SystemEvent" 
    system_name: str = None

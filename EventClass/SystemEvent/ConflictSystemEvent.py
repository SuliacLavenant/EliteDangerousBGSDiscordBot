from EventClass.SystemEvent.SystemEvent import SystemEvent

class ConflictSystemEvent(SystemEvent):
    conflict: str # war or election
    minor_faction_names: tuple # (minor_faction_1_name, minor_faction_2_name)
    system_name: str

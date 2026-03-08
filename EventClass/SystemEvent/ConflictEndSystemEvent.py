from EventClass.SystemEvent.ConflictSystemEvent import ConflictSystemEvent

class ConflictEndSystemEvent(ConflictSystemEvent):
    conflict: str # war or election
    minor_faction_names: tuple # (minor_faction_1_name, minor_faction_2_name)
    system_name: str
    winner: int # None, 0, 1 

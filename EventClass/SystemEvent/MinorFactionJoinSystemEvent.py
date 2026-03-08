from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

class MinorFactionJoinSystemEvent(MinorFactionSystemEvent):
    minor_faction_name: str
    system_name: str

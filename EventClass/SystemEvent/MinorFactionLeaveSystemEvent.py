from EventClass.SystemEvent.MinorFactionSystemEvent import MinorFactionSystemEvent

class MinorFactionLeaveSystemEvent(MinorFactionSystemEvent):
    minor_faction_name: str
    system_name: str

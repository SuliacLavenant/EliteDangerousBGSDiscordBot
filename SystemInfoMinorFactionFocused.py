
class SystemInfoMinorFactionFocused:
    systemName = ""
    minorFactionName = ""
    controllingFaction = ""
    positionInSystem = -1
    influence = -1

    states = []

    date = -1
    dateStr = ""

    def __init__(self, systemName: str, minorFactionName: str):
        self.systemName = systemName
        self.minorFactionName = minorFactionName

    def setDate(self, date: str):
        self.date = date
        self.dateStr = f"{date[8:10]} {date[5:7]} {date[0:4]}, {date[11:16]}"
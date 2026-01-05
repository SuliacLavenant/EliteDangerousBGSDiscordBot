from BotConfig.Emotes.System.Information import Information

class System:
    information: Information
    numberOfMinorFaction: dict

    def __init__(self, emotesDict: dict):
        self.information = Information(emotesDict["information"])

        self.numberOfMinorFaction = {}
        self.numberOfMinorFaction[3] = emotesDict["numberOfMinorFaction"]["minimum"]
        self.numberOfMinorFaction[4] = emotesDict["numberOfMinorFaction"]["4"]
        self.numberOfMinorFaction[5] = emotesDict["numberOfMinorFaction"]["5"]
        self.numberOfMinorFaction[6] = emotesDict["numberOfMinorFaction"]["6"]
        self.numberOfMinorFaction[7] = emotesDict["numberOfMinorFaction"]["maximum"]

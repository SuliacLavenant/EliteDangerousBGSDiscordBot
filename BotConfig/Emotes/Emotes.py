from BotConfig.Emotes.SystemInformation import SystemInformation
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction

class Emotes:
    systemInformation: SystemInformation
    minorFaction: MinorFaction

    def __init__(self, emotesDict: dict):
        self.systemInformation = SystemInformation(emotesDict["systemInformation"])
        self.minorFaction = MinorFaction(emotesDict["minorFaction"])

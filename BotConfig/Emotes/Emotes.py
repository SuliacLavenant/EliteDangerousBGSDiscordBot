from BotConfig.Emotes.System.System import System
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction

class Emotes:
    system: System
    minorFaction: MinorFaction

    def __init__(self, emotesDict: dict):
        self.system = System(emotesDict["system"])
        self.minorFaction = MinorFaction(emotesDict["minorFaction"])

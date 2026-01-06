from BotConfig.Emotes.System.System import System
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction

class Emotes:
    warning: str
    system: System
    minorFaction: MinorFaction

    def __init__(self, emotesDict: dict):
        self.warning = emotesDict["warning"]
        self.system = System(emotesDict["system"])
        self.minorFaction = MinorFaction(emotesDict["minorFaction"])

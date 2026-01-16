from BotConfig.Emotes.Data import Data
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction
from BotConfig.Emotes.System.System import System

class Emotes:
    data: Data
    warning: str
    nothing: str
    systems: str
    system: System
    minorFaction: MinorFaction

    def __init__(self, emotesDict: dict):
        self.data = Data(emotesDict["data"])
        self.warning = emotesDict["warning"]
        self.nothing = emotesDict["nothing"]
        self.systems = emotesDict["systems"]
        self.system = System(emotesDict["system"])
        self.minorFaction = MinorFaction(emotesDict["minorFaction"])

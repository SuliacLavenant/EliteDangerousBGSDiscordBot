from BotConfig.Emotes.Arrow import Arrow
from BotConfig.Emotes.Data import Data
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction
from BotConfig.Emotes.Mission.Mission import Mission
from BotConfig.Emotes.System.System import System

class Emotes:
    arrow: Arrow
    data: Data
    warning: str
    nothing: str
    pin: str
    systems: str
    system: System
    minorFaction: MinorFaction
    mission: Mission
    target: str

    def __init__(self, emotesDict: dict):
        self.arrow = Arrow(emotesDict["arrow"])
        self.data = Data(emotesDict["data"])
        self.warning = emotesDict["warning"]
        self.nothing = emotesDict["nothing"]
        self.pin = emotesDict["pin"]
        self.systems = emotesDict["systems"]
        self.system = System(emotesDict["system"])
        self.minorFaction = MinorFaction(emotesDict["minorFaction"])
        self.mission = Mission(emotesDict["mission"])
        self.target = emotesDict["target"]

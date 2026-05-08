from BotConfig.Emotes.Arrow import Arrow
from BotConfig.Emotes.Data import Data
from BotConfig.Emotes.MinorFaction.MinorFaction import MinorFaction
from BotConfig.Emotes.Mission.Mission import Mission
from BotConfig.Emotes.Squadron.Squadron import Squadron
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
    squadron: Squadron
    target: str

    def __init__(self, emote_dict: dict):
        self.arrow = Arrow(emote_dict["arrow"])
        self.data = Data(emote_dict["data"])
        self.warning = emote_dict["warning"]
        self.nothing = emote_dict["nothing"]
        self.pin = emote_dict["pin"]
        self.systems = emote_dict["systems"]
        self.system = System(emote_dict["system"])
        self.minorFaction = MinorFaction(emote_dict["minorFaction"])
        self.mission = Mission(emote_dict["mission"])
        self.squadron = Squadron(emote_dict["squadron"])
        self.target = emote_dict["target"]

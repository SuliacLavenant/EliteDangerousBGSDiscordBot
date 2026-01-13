from BotConfig.Emotes.MinorFaction.PositionInSystem import PositionInSystem
from BotConfig.Emotes.MinorFaction.State import State

class MinorFaction:
    positionInSystem: PositionInSystem
    state: State

    def __init__(self, emotesDict: dict):
        self.positionInSystem = PositionInSystem(emotesDict["positionInSystem"])
        self.state = State(emotesDict["state"])

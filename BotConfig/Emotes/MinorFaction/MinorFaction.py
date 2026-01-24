from BotConfig.Emotes.MinorFaction.Influence import Influence
from BotConfig.Emotes.MinorFaction.PositionInSystem import PositionInSystem
from BotConfig.Emotes.MinorFaction.State import State

class MinorFaction:
    influence: Influence
    positionInSystem: PositionInSystem
    state: State

    def __init__(self, emotesDict: dict):
        self.influence = Influence(emotesDict["influence"])
        self.positionInSystem = PositionInSystem(emotesDict["positionInSystem"])
        self.state = State(emotesDict["state"])

from BotConfig.BGS.State.Expansion import Expansion
from BotConfig.BGS.State.Retreat import Retreat

class State:
    expansion: Expansion
    retreat: Retreat

    def __init__(self, state_dict: dict):
        self.expansion = Expansion(state_dict["expansion"])
        self.retreat = Retreat(state_dict["retreat"])

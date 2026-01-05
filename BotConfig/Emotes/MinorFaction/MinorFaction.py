from BotConfig.Emotes.MinorFaction.State import State

class MinorFaction:
    state: State

    def __init__(self, emotesDict: dict):
        self.state = State(emotesDict["state"])

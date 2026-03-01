from BotConfig.Emotes.Mission.State import State

class Mission:
    state: State

    def __init__(self, emote_dict: dict):
        self.state = State(emote_dict["state"])

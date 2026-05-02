from BotConfig.Emotes.Mission.State import State

class Mission:
    mission: str
    state: State

    def __init__(self, emote_dict: dict):
        self.mission = emote_dict["mission"]
        self.state = State(emote_dict["state"])

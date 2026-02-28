from BotConfig.BGS.State.State import State

class BGS:
    state: State

    def __init__(self, bgs_dict: dict):
        self.state = State(bgs_dict["state"])

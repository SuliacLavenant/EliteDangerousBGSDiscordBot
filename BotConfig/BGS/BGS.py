from BotConfig.BGS.LeaderInfluenceWarning import LeaderInfluenceWarning
from BotConfig.BGS.State.State import State

class BGS:
    leader_influence_warning: LeaderInfluenceWarning
    state: State

    def __init__(self, bgs_dict: dict):
        self.leader_influence_warning = LeaderInfluenceWarning(bgs_dict["leader_influence_warning"])
        self.state = State(bgs_dict["state"])

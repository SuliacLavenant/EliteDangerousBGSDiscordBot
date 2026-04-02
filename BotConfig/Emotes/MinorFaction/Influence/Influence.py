from BotConfig.Emotes.MinorFaction.Influence.LeaderInfluenceWarning import LeaderInfluenceWarning
class Influence:
    down: str
    leader_influence_warning: LeaderInfluenceWarning
    up: str

    def __init__(self, emotesDict: dict):
        self.down = emotesDict["down"]
        self.leader_influence_warning = LeaderInfluenceWarning(emotesDict["leader_influence_warning"])
        self.up = emotesDict["up"]

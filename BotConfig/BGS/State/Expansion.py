class Expansion:
    trigger_influence: float
    warning_influence: float

    def __init__(self, expansion_dict: dict):
        self.trigger_influence = expansion_dict["trigger_influence"]
        self.warning_influence = expansion_dict["warning_influence"]

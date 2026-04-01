class Retreat:
    trigger_influence: float

    def __init__(self, retreat_dict: dict):
        self.trigger_influence = retreat_dict["trigger_influence"]
        self.warning_influence = retreat_dict["warning_influence"]

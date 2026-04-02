class LeaderInfluenceWarning:
    level1: float
    level2: float
    level3: float

    def __init__(self, bgs_dict: dict):
        self.level1 = bgs_dict["level1"]
        self.level2 = bgs_dict["level2"]
        self.level3 = bgs_dict["level3"]

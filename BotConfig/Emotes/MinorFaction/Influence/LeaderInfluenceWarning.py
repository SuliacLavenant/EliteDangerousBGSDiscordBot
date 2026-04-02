class LeaderInfluenceWarning:
    level0: str
    level1: str
    level2: str
    level3: str

    def __init__(self, emotesDict: dict):
        self.level0 = emotesDict["level0"]
        self.level1 = emotesDict["level1"]
        self.level2 = emotesDict["level2"]
        self.level3 = emotesDict["level3"]

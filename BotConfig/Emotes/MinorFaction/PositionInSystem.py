class PositionInSystem:
    leader: str
    diplomatic: str
    none: str
    other: str

    def __init__(self, emotesDict: dict):
        self.leader = emotesDict["leader"]
        self.diplomatic = emotesDict["diplomatic"]
        self.none = emotesDict["none"]
        self.other = emotesDict["other"]
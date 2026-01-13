class PositionInSystem:
    leader: str
    diplomatic: str
    other: str

    def __init__(self, emotesDict: dict):
        self.leader = emotesDict["leader"]
        self.diplomatic = emotesDict["diplomatic"]
        self.other = emotesDict["other"]
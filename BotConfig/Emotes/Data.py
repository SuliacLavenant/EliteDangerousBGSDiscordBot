class Data:
    online: str
    save: str
    saved: str
    tracked: str
    untracked: str

    def __init__(self, emotesDict: dict):
        self.online = emotesDict["online"]
        self.save = emotesDict["save"]
        self.saved = emotesDict["saved"]
        self.tracked = emotesDict["tracked"]
        self.untracked = emotesDict["untracked"]

class Data:
    online: str
    save: str
    saved: str

    def __init__(self, emotesDict: dict):
        self.online = emotesDict["online"]
        self.save = emotesDict["save"]
        self.saved = emotesDict["saved"]

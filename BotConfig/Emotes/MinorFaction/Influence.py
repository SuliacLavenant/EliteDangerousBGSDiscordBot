class Influence:
    down: str
    up: str

    def __init__(self, emotesDict: dict):
        self.down = emotesDict["down"]
        self.up = emotesDict["up"]

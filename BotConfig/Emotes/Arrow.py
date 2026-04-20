class Arrow:
    down: str
    left: str
    right: str
    up: str

    def __init__(self, emotesDict: dict):
        self.down = emotesDict["down"]
        self.left = emotesDict["left"]
        self.right = emotesDict["right"]
        self.up = emotesDict["up"]

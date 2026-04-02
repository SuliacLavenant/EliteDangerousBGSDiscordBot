class State:
    none: str
    war: str
    election: str
    expansion: str
    retreat: str

    def __init__(self, emotesDict: dict):
        self.none = emotesDict["none"]
        self.war = emotesDict["war"]
        self.election = emotesDict["election"]
        self.expansion = emotesDict["expansion"]
        self.expansion_warning = emotesDict["expansion_warning"]
        self.important = emotesDict["important"]
        self.retreat = emotesDict["retreat"]
        self.retreat_warning = emotesDict["retreat_warning"]

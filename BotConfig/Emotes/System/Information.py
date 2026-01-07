import json

class Information:
    economy: str
    population: str
    security: str
    architect: str
    origin: str

    def __init__(self, emotesDict: dict):
        self.economy = emotesDict["economy"]
        self.population = emotesDict["population"]
        self.security = emotesDict["security"]
        self.architect = emotesDict["architect"]
        self.origin = emotesDict["origin"]


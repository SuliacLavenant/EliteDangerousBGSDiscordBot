import json

class SystemInformation:
    economy: str
    population: str
    security: str
    architect: str

    def __init__(self, emotesDict: dict):
        self.economy = emotesDict["economy"]
        self.population = emotesDict["population"]
        self.security = emotesDict["security"]
        self.architect = emotesDict["architect"]


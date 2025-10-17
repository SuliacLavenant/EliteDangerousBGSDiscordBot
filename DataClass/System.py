class System:
    name = ""
    population = -1
    controllingFaction = ""
    factions = {}

    def __init__(self, name: str, population: int, controllingFaction: str):
        self.name = name
        self.population = population
        self.controllingFaction = controllingFaction

    def addFaction(self, name: str, allegiance: str, government: str, influence: int, state: str):
        self.factions[name] = {"name": name, "allegiance": allegiance, "government": government, "influence": influence, "state": state}
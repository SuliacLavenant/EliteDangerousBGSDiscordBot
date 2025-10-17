class MinorFaction:
    name = ""
    allegiance = ""
    government = ""
    population = -1

    def __init__(self, name: str, allegiance: str, government: str, population: int):
        self.name = name
        self.allegiance = allegiance
        self.government = government
        self.population = population

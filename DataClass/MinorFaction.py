from dataclasses import dataclass, field

#TODO add controlled systems
@dataclass
class MinorFaction:
    name: str = ""
    allegiance: str = ""
    government: str = ""
    numberOfSystems: int = -1

    def __init__(self, name: str, allegiance: str, government: str):
        self.name = name
        self.allegiance = allegiance
        self.government = government

    def setNumberOfSystems(self, numberOfSystems: int):
        self.numberOfSystems = numberOfSystems

    def __str__(self):
        return f"Minor Faction: {self.name.title()} | Allegiance: {self.allegiance.title()} | Government: {self.government.title()} | Present in {self.numberOfSystems} systems"


from dataclasses import dataclass, field

#TODO add controlled systems
@dataclass
class MinorFaction:
    name: str = ""
    allegiance: str = ""
    government: str = ""
    capital: str = ""
    numberOfSystems: int = -1

    @classmethod
    def initFromStoredData(cls, minorFactionData: dict):
        return cls(name=minorFactionData["name"], allegiance=minorFactionData["allegiance"], government=minorFactionData["government"], capital=minorFactionData["capital"])

    def setNumberOfSystems(self, numberOfSystems: int):
        self.numberOfSystems = numberOfSystems

    def __str__(self):
        return f"Minor Faction: {self.name.title()} | Allegiance: {self.allegiance.title()} | Government: {self.government.title()} | Capital: {self.capital.title()} | Present in {self.numberOfSystems} systems"


from dataclasses import dataclass, field

@dataclass
class DiplomaticSystem:
    systemName: str = ""
    diplomaticPositions: dict[str, int] = field(default_factory=dict) # minorFactionName: position | position -> 0: in system, 1: leader, 2: second...
    description: str = ""

    def __post_init__(self):
        self.systemName = self.systemName.lower()

    @classmethod
    def initFromStoredData(cls, diplomaticPositionInSystemData: dict):
        return cls(systemName=diplomaticPositionInSystemData["systemName"],diplomaticPositions=diplomaticPositionInSystemData["diplomaticPositions"],description=diplomaticPositionInSystemData["description"])

    def addMinorFactionDiplomaticPosition(self, minorFactionName: str, position: int):
        self.diplomaticPositions[minorFactionName.lower()] = position

    def __str__(self):
        return f"Diplomatic System Name: \"{self.systemName}\" | Diplomatic Positions: {self.diplomaticPositions} | Description: \"{self.description}\""

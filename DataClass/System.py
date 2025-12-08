from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class System:
    name: str = ""
    population: int = -1
    security: str = ""
    economy: str = ""
    secondEconomy: str = ""
    reserve: str = ""

    controllingFaction: str = ""
    factions: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def initFromStoredData(cls, systemData: dict):
        return cls(name=systemData["name"], population=systemData["population"], security=systemData["security"], economy=systemData["economy"], secondEconomy=systemData["secondEconomy"], reserve=systemData["reserve"], controllingFaction=systemData["controllingFaction"], factions=systemData["factions"])

    def addFaction(self, name: str, allegiance: str, government: str, influence: int, pendingStates: list, activeStates: list, recoveringStates: list):
        self.factions[self.lower(name)] = {"name": self.lower(name), "allegiance": self.lower(allegiance), "government": self.lower(government), "influence": influence, "pendingStates": pendingStates, "activeStates": activeStates, "recoveringStates": recoveringStates}


    ### Method
    def isControlledBy(self, minorFactionName: str):
        return self.controllingFaction == minorFactionName

    # Check if leader influence difference is safe
    def isLeaderSafe(self, safePercentDifference: int):
        safe = True
        leaderInfluence = self.factions[self.controllingFaction]["influence"]

        for faction in self.factions:
            if faction!=self.controllingFaction:
                factionInfluence = self.factions[faction]["influence"]
                safe = safe and ((leaderInfluence-factionInfluence)>safePercentDifference)

        return safe


    # Return influence difference between leader and second 
    def getLeaderInfluence(self):
        return self.factions[self.controllingFaction]["influence"]

    # Return influence difference between leader and second 
    def getLeaderInfluenceMargin(self):
        leaderInfluence = self.getLeaderInfluence()
        secondInfluence = 0

        for faction in self.factions:
            if faction!=self.controllingFaction:
                factionInfluence = self.factions[faction]["influence"]
                if factionInfluence>secondInfluence:
                    secondInfluence = factionInfluence

        return leaderInfluence-secondInfluence

    
    # Return name and influence of the second 
    def getSecondAndItsInfluence(self):
        leaderInfluence = self.factions[self.controllingFaction]["influence"]
        secondInfluence = 0
        second = ""

        for faction in self.factions:
            if faction!=self.controllingFaction:
                factionInfluence = self.factions[faction]["influence"]
                if factionInfluence>secondInfluence:
                    secondInfluence = factionInfluence
                    second = faction

        return (second,secondInfluence)

    
    # Return influence of the minor faction
    def getMinorFactionInfluence(self, minorFactionName: str):
        if minorFactionName in self.factions:
            return self.factions[minorFactionName]["influence"]
        else:
            return 0

    def doMinorFactionHaveState(self, minorFactionName: str, state: str):
        if state in self.factions[minorFactionName]["pendingStates"]:
            return "pending"
        elif state in self.factions[minorFactionName]["activeStates"]:
            return "active"
        elif state in self.factions[minorFactionName]["recoveringStates"]:
            return "recovering"
        else:
            return None
        
    def getMinorFactionConflictState(self, minorFactionName: str):
        war = self.doMinorFactionHaveState(minorFactionName, "war")
        if war == "pending" or war == "active":
            return "war"
        civilWar = self.doMinorFactionHaveState(minorFactionName, "civil war")
        if civilWar == "pending" or civilWar == "active":
            return "civil war"
        election = self.doMinorFactionHaveState(minorFactionName, "election")
        if election == "pending" or election == "active":
            return "election"
        return None

    def lower(self, string: str):
        return string.lower() if isinstance(string, str) else string

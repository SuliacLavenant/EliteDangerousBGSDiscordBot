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

    controllingFactionName: str = ""
    factions: dict[str, dict] = field(default_factory=dict)

    isOrigin: bool = False
    isArchitected: bool = False
    architect: str = ""
    isDiplomatic: bool = False

    lastInfluenceUpdate: int = 0 #unix time

    def __post_init__(self):
        self.name = self.name.lower()
        self.security = self.security.lower()
        self.economy = self.economy.lower()
        self.secondEconomy = self.secondEconomy.lower() if self.secondEconomy!=None else None
        self.reserve = self.reserve.lower() if self.reserve!=None else None
        self.controllingFactionName = self.controllingFactionName.lower()
        self.architect = self.architect.lower()

    @classmethod
    def initFromStoredData(cls, systemData: dict):
        return cls(name=systemData["name"], population=systemData["population"], security=systemData["security"], economy=systemData["economy"], secondEconomy=systemData["secondEconomy"], reserve=systemData["reserve"], controllingFactionName=systemData["controllingFactionName"], factions=systemData["factions"], isOrigin=systemData["isOrigin"], isArchitected=systemData["isArchitected"], architect=systemData["architect"], isDiplomatic=systemData["isDiplomatic"], lastInfluenceUpdate=systemData["lastInfluenceUpdate"])

    def addFaction(self, name: str, allegiance: str, government: str, influence: int, pendingStates: list, activeStates: list, recoveringStates: list):
        self.factions[self.lower(name)] = {"name": self.lower(name), "allegiance": self.lower(allegiance), "government": self.lower(government), "influence": influence, "pendingStates": pendingStates, "activeStates": activeStates, "recoveringStates": recoveringStates}

    def update(self, systemNew):
        self.population = systemNew.population
        self.security = systemNew.security
        self.economy = systemNew.economy
        self.secondEconomy = systemNew.secondEconomy
        self.controllingFactionName = systemNew.controllingFactionName
        self.factions = systemNew.factions

        self.lastInfluenceUpdate = systemNew.lastInfluenceUpdate



    ### Method
    def isControlledBy(self, minorFactionName: str):
        return self.controllingFactionName == minorFactionName

    # Check if leader influence difference is safe
    def isLeaderSafe(self, safePercentDifference: int):
        safe = True
        leaderInfluence = self.factions[self.controllingFactionName]["influence"]

        for faction in self.factions:
            if faction!=self.controllingFactionName:
                factionInfluence = self.factions[faction]["influence"]
                safe = safe and ((leaderInfluence-factionInfluence)>safePercentDifference)

        return safe


    def getMinorFactionPosition(self, minorFactionName: str) -> int:
        if minorFactionName not in self.factions.keys():
            return -1
        elif self.isControlledBy(minorFactionName):
            return 1
        else:
            position = 1
            influence = self.factions[minorFactionName]["influence"]
            for faction in self.factions:
                if faction!=minorFactionName:
                    if influence < self.factions[faction]["influence"]:
                        position+=1
            return position



    # Return influence difference between leader and second 
    def getLeaderInfluence(self):
        return self.factions[self.controllingFactionName]["influence"]

    # Return influence difference between leader and second 
    def getLeaderInfluenceMargin(self):
        leaderInfluence = self.getLeaderInfluence()
        secondInfluence = 0

        for faction in self.factions:
            if faction!=self.controllingFactionName:
                factionInfluence = self.factions[faction]["influence"]
                if factionInfluence>secondInfluence:
                    secondInfluence = factionInfluence

        return leaderInfluence-secondInfluence

    
    # Return name and influence of the second 
    def getSecondAndItsInfluence(self):
        leaderInfluence = self.factions[self.controllingFactionName]["influence"]
        secondInfluence = 0
        second = ""

        for faction in self.factions:
            if faction!=self.controllingFactionName:
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
        if self.doMinorFactionHaveTheSameInfluenceAsAnother(minorFactionName):
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
    
    def doMinorFactionHaveTheSameInfluenceAsAnother(self, minorFactionName: str):
        minorFactionInfluence = self.factions[minorFactionName]["influence"]
        for factionName in self.factions:
            if factionName != minorFactionName:
                factionInfluence = self.factions[factionName]["influence"]
                if factionInfluence == minorFactionInfluence:
                    return True
        return False

    def lower(self, string: str):
        return string.lower() if isinstance(string, str) else string




##########################################################################################################
###################################### STR Functions #####################################################
##########################################################################################################

    def getStrSystemEconomy(self):
        if self.secondEconomy == None:
            return self.economy.title()
        else:
            return f"{self.economy.title()} / {self.secondEconomy.title()}"
        
    def getStrSystemPopulation(self):
        if self.population == -1:
            return "?"
        match len(str(self.population)):
            case 0 | 1 | 2 | 3:
                return str(self.population)
            case 4 | 5 | 6:
                return f"{str(self.population)[:3]},{str(self.population)[3:]}"
            case 7 | 8 | 9:
                return f"{str(round(self.population/1000000,2))} million"
            case _:
                return f"{str(round(self.population/1000000000,2))} billion"

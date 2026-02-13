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
    isArchitected: bool = None
    architect: str = ""
    isDiplomatic: bool = False

    lastInfluenceUpdate: int = 0 #unix time

    isStored: int = False #stored system

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
        return cls(name=systemData["name"], population=systemData["population"], security=systemData["security"], economy=systemData["economy"], secondEconomy=systemData["secondEconomy"], reserve=systemData["reserve"], controllingFactionName=systemData["controllingFactionName"], factions=systemData["factions"], isOrigin=systemData["isOrigin"], isArchitected=systemData["isArchitected"], architect=systemData["architect"], isDiplomatic=systemData["isDiplomatic"], lastInfluenceUpdate=systemData["lastInfluenceUpdate"], isStored=True)

    def addFaction(self, name: str, allegiance: str, government: str, influence: int, pendingStates: list, activeStates: list, recoveringStates: list):
        self.factions[self.lower(name)] = {"name": self.lower(name), "allegiance": self.lower(allegiance), "government": self.lower(government), "influence": influence, "pendingStates": pendingStates, "activeStates": activeStates, "recoveringStates": recoveringStates}

    def update(self, systemNew):
        if systemNew!=None:
            self.population = systemNew.population
            self.security = systemNew.security
            self.economy = systemNew.economy
            self.secondEconomy = systemNew.secondEconomy
            self.controllingFactionName = systemNew.controllingFactionName
            self.factions = systemNew.factions

            self.lastInfluenceUpdate = systemNew.lastInfluenceUpdate


    ### Method
    def isControlledBy(self, minor_faction_name: str):
        return self.controllingFactionName == minor_faction_name


    def haveFaction(self, minor_faction_name: str):
        return minor_faction_name in self.factions


    # Check if leader influence difference is safe
    def isLeaderSafe(self, safePercentDifference: int):
        safe = True
        leaderInfluence = self.factions[self.controllingFactionName]["influence"]

        for faction in self.factions:
            if faction!=self.controllingFactionName:
                factionInfluence = self.factions[faction]["influence"]
                safe = safe and ((leaderInfluence-factionInfluence)>safePercentDifference)

        return safe


    def getMinorFactionPosition(self, minor_faction_name: str) -> int:
        if minor_faction_name not in self.factions.keys():
            return -1
        elif self.isControlledBy(minor_faction_name):
            return 1
        else:
            position = 1
            influence = self.factions[minor_faction_name]["influence"]
            for faction in self.factions:
                if faction!=minor_faction_name:
                    if influence < self.factions[faction]["influence"]:
                        position+=1
            return position


    def getMinorFactionsRanking(self):
        ranking = {}
        for minor_faction_name in self.factions:
            rank = self.getMinorFactionPosition(minor_faction_name)
            if rank in ranking.keys():
                ranking[rank+1] = minor_faction_name
            else:
                ranking[rank] = minor_faction_name
        return ranking


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
    def getMinorFactionInfluence(self, minor_faction_name: str):
        if minor_faction_name in self.factions:
            return self.factions[minor_faction_name]["influence"]
        else:
            return 0

    def doMinorFactionHaveState(self, minor_faction_name: str, state: str):
        if state in self.factions[minor_faction_name]["pendingStates"]:
            return "pending"
        elif state in self.factions[minor_faction_name]["activeStates"]:
            return "active"
        elif state in self.factions[minor_faction_name]["recoveringStates"]:
            return "recovering"
        else:
            return None
        
    def getMinorFactionConflictState(self, minor_faction_name: str):
        if self.doMinorFactionHaveTheSameInfluenceAsAnother(minor_faction_name):
            war = self.doMinorFactionHaveState(minor_faction_name, "war")
            if war == "pending" or war == "active":
                return "war"
            civilWar = self.doMinorFactionHaveState(minor_faction_name, "civil war")
            if civilWar == "pending" or civilWar == "active":
                return "civil war"
            election = self.doMinorFactionHaveState(minor_faction_name, "election")
            if election == "pending" or election == "active":
                return "election"
        return None
    
    def doMinorFactionHaveTheSameInfluenceAsAnother(self, minor_faction_name: str):
        minorFactionInfluence = self.factions[minor_faction_name]["influence"]
        for factionName in self.factions:
            if factionName != minor_faction_name:
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

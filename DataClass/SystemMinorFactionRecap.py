from dataclasses import dataclass, field
from copy import deepcopy

from BotConfig import BotConfig
from DataClass.System import System

@dataclass
class SystemMinorFactionRecap:
    name: str = ""
    influence: int = -1
    isLeader: bool = None
    leaderInfluenceMargin: int = None
    influenceWarningLevel: int = -1
    isArchitect: bool = None
    leaderInfluence: int = -1

    expansionWarning: bool = False
    retreatWarning: bool = False

    warning: str = None
    importantState: str = None
    positionInSystem: str = None
    numberOfFactions: int = 0

    def __init__(self, system: System, minorFactionName: str):
        self.system = system
        self.minorFactionName = minorFactionName

        self.influence = system.getMinorFactionInfluence(self.minorFactionName)
        self.leaderInfluence = system.getLeaderInfluence()
        self.isLeader = system.isControlledBy(self.minorFactionName)
        if self.isLeader:
            self.leaderInfluenceMargin = self.system.getLeaderInfluenceMargin()
            self.calculateLeaderInfluenceMarginWarning()

        self.checkRetreatWarning()
        self.checkExpansionWarning()

        self.checkImportantState()
        self.checkPositionInSystem()
        self.checkInfluenceWarning()
        self.numberOfFactions = len(system.factions)


    #Calculate influence warning
    def checkInfluenceWarning(self):
        if self.isLeader:
            self.warning = self.calculateLeaderInfluenceMarginWarning()
        if self.retreatWarning:
            self.warning = "retreat"
        if self.expansionWarning:
            self.warning = "expansion"
        if self.importantState != None:
            self.warning = "state"

    def calculateLeaderInfluenceMarginWarning(self):
        if self.leaderInfluenceMargin <= BotConfig.leaderInfluenceWarning["level3"]:
            return "marginLvl3"
        elif self.leaderInfluenceMargin <= BotConfig.leaderInfluenceWarning["level2"]:
            return "marginLvl2"
        elif self.leaderInfluenceMargin < BotConfig.leaderInfluenceWarning["level1"]:
            return "marginLvl1"
        else:
            return "marginLvl0"

    def checkExpansionWarning(self):
        self.expansionWarning = self.system.getMinorFactionInfluence(self.minorFactionName)>=BotConfig.influenceExpansionWarning

    def checkRetreatWarning(self):
        self.retreatWarning = self.system.getMinorFactionInfluence(self.minorFactionName)<=BotConfig.influenceRetreatWarning or self.system.doMinorFactionHaveState(self.minorFactionName, "retreat") != None


    def checkImportantState(self):
        if self.retreatWarning:
            self.importantState = "retreat"
        conflictState = self.system.getMinorFactionConflictState(self.minorFactionName)
        if conflictState!=None:
            self.importantState = conflictState


    def checkPositionInSystem(self):
        if self.isLeader:
            self.positionInSystem = "leader"
        else:
            self.positionInSystem = "other"


    def __str__(self):
        if self.isLeader:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | leader, influence warning level {self.influenceWarningLevel} ({round(self.leaderInfluenceMargin*100, 2)}% margin) | architect {self.isArchitect}"
        else:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | architect {self.isArchitect}"

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
    numberOfFactions: int = -1
    leaderInfluence: int = -1
    retreatWarning: bool = False
    conflictState: str = None

    def __init__(self, system: System, minorFactionName: str):
        self.name = system.name
        self.influence = system.getMinorFactionInfluence(minorFactionName)
        self.numberOfFactions = len(system.factions)
        self.isLeader = system.isControlledBy(minorFactionName)
        if self.isLeader:
            self.leaderInfluenceMargin = system.getLeaderInfluenceMargin()
            self.calculateInfluenceWarningLevel()
        self.leaderInfluence = system.getLeaderInfluence()
        self.checkRetreatWarning(system, minorFactionName)
        self.checkConflictState(system, minorFactionName)


    #Calculate influence warning
    def calculateInfluenceWarningLevel(self):
        if self.leaderInfluenceMargin <= BotConfig.leaderInfluenceWarning["level3"]:
            self.influenceWarningLevel = 3
        elif self.leaderInfluenceMargin <= BotConfig.leaderInfluenceWarning["level2"]:
            self.influenceWarningLevel = 2
        elif self.leaderInfluenceMargin < BotConfig.leaderInfluenceWarning["level1"]:
            self.influenceWarningLevel = 1
        else:
            self.influenceWarningLevel = 0


    def checkRetreatWarning(self, system: System, minorFactionName: str):
        if system.getMinorFactionInfluence(minorFactionName)<=BotConfig.influenceRetreatWarning or system.doMinorFactionHaveState(minorFactionName, "retreat") != None:
            self.retreatWarning = True
        else:
            self.retreatWarning = False


    def checkConflictState(self, system: System, minorFactionName: str):
        self.conflictState = system.getMinorFactionConflictState(minorFactionName)


    def __str__(self):
        if self.isLeader:
            return f"{self.name} — influence {round(self.influence*100, 2)}% | leader, influence warning level {self.influenceWarningLevel} ({round(self.leaderInfluenceMargin*100, 2)}% margin) | architect {self.isArchitect}"
        else:
            return f"{self.name} — influence {round(self.influence*100, 2)}% | architect {self.isArchitect}"

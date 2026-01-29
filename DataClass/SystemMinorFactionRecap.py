from dataclasses import dataclass, field
from copy import deepcopy
from datetime import datetime, timezone

from BotConfig.BotConfig import BotConfig
from DataClass.System import System
from DataClass.DiplomaticSystem import DiplomaticSystem
from DataClass.SystemGroup import SystemGroup

@dataclass
class SystemMinorFactionRecap:
    system: System
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

    marginWarning: bool = False

    daysSinceLastUpdate: int = -1

    isOrigin: bool = False
    isArchitect: bool = False

    isDiplomatic: bool = False
    diplomaticWarning: str = None


    systemGroup: SystemGroup = None

    def __init__(self, system: System, minorFactionName: str, diplomaticSystem: DiplomaticSystem = None):
        self.system = system
        self.minorFactionName = minorFactionName
        self.isDiplomatic = self.system.isDiplomatic
        self.diplomaticSystem = diplomaticSystem

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
        self.checkDiplomaticPosition()

        self.numberOfFactions = len(system.factions)

        self.calculateDaysSinceLastUpdate()


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
            self.marginWarning = True
            self.influenceWarningLevel = 3
            return "marginLvl3"
        elif self.leaderInfluenceMargin <= BotConfig.leaderInfluenceWarning["level2"]:
            self.marginWarning = True
            self.influenceWarningLevel = 2
            return "marginLvl2"
        elif self.leaderInfluenceMargin < BotConfig.leaderInfluenceWarning["level1"]:
            self.marginWarning = True
            self.influenceWarningLevel = 1
            return "marginLvl1"
        else:
            self.influenceWarningLevel = 0
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
        elif self.isDiplomatic:
            self.positionInSystem = "diplomatic"
        else:
            self.positionInSystem = "other"


    def checkDiplomaticPosition(self):
        if self.system.isDiplomatic:
            if self.minorFactionName in self.diplomaticSystem.diplomaticPositions.keys():
                minorFactionPosition = self.system.getMinorFactionPosition(self.minorFactionName)
                match self.diplomaticSystem.diplomaticPositions[self.minorFactionName]:
                    case 1:
                        if minorFactionPosition != 1:
                            self.diplomaticWarning = "shouldBeLeader"
                    case 2:
                        if minorFactionPosition == 1:
                            self.diplomaticWarning = "shouldNotBeLeader"
                        elif minorFactionPosition == 2:
                            self.diplomaticWarning = "notLeaderGood"
                        else:
                            self.diplomaticWarning = "shouldtBeSecond"
                    case _:
                        for otherMinoFactionName in self.diplomaticSystem.diplomaticPositions.keys():
                            if self.diplomaticSystem.diplomaticPositions[otherMinoFactionName] == 1:
                                if self.system.getMinorFactionPosition(otherMinoFactionName) != 1 and minorFactionPosition == 1:
                                    self.diplomaticWarning = "shouldNotBeLeader"
                                else:
                                    self.diplomaticWarning = "notLeaderGood"


    def calculateDaysSinceLastUpdate(self):
        currentTime = datetime.now(timezone.utc)
        lastInfluenceUpdate = datetime.fromtimestamp(self.system.lastInfluenceUpdate, tz=timezone.utc)
        delta = currentTime - lastInfluenceUpdate
        self.daysSinceLastUpdate = delta.days


    def __str__(self):
        if self.isLeader:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | leader, influence warning level {self.influenceWarningLevel} ({round(self.leaderInfluenceMargin*100, 2)}% margin) | architect {self.isArchitect}"
        else:
            return f"{self.system.name} — influence {round(self.influence*100, 2)}% | architect {self.isArchitect}"

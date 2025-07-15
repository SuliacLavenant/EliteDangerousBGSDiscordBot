
class SystemInfoMinorFactionFocused:
    systemName = ""
    minorFactionName = ""
    controllingFaction = ""
    positionInSystem = -1
    influence = -1

    population = -1
    populationStr = ""

    states = []

    date = -1
    dateStr = ""

    def __init__(self, systemName: str, minorFactionName: str):
        self.systemName = systemName
        self.minorFactionName = minorFactionName

    def setDate(self, date: str):
        self.date = date
        self.dateStr = f"{date[8:10]} {date[5:7]} {date[0:4]}, {date[11:16]}"

    def setPopulation(self, population: int):
        self.population = population
        popStr=str(self.population)

        if self.population>=1000:
            self.populationStr = f"{self.population//1000},{popStr[-3:]}"
        elif self.population>=1000000:
            self.populationStr = f"{self.population//1000000}.{popStr[-6:-4]} million"
        elif self.population>=1000000000:
            self.populationStr = f"{self.population//1000000000}.{popStr[-9:-7]} billion"

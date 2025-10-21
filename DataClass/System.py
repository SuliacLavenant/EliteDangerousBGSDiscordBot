class System:
    name = ""
    population = -1
    security = ""
    economy = ""
    secondEconomy = ""
    reserve = ""

    controllingFaction = ""
    factions = {}

    def initFromAPI(self, name: str, population: int, security: str, economy: str, secondEconomy: str, reserve: str, controllingFaction: str):
        self.name = self.lower(name)
        self.population = population
        self.security = self.lower(security)
        self.economy = self.lower(economy)
        self.secondEconomy = self.lower(secondEconomy)
        self.reserve = self.lower(reserve)
        self.controllingFaction = self.lower(controllingFaction)

    def addFaction(self, name: str, allegiance: str, government: str, influence: int, state: str):
        self.factions[name] = {"name": self.lower(name), "allegiance": self.lower(allegiance), "government": self.lower(government), "influence": influence, "state": self.lower(state)}

    #init from stored data
    def initFromStoredData(self, systemData: dict):
        self.name = systemData["name"]
        self.population = systemData["population"]
        self.security = systemData["security"]
        self.economy = systemData["economy"]
        self.secondEconomy = systemData["secondEconomy"]
        self.reserve = systemData["reserve"]
        self.controllingFaction = systemData["controllingFaction"]

    ### Method
    def isControlledBy(self, minorFactionName: str):
        return self.controllingFaction == minorFactionName

    ###

    def lower(self, string: str):
        return string.lower() if isinstance(string, str) else string
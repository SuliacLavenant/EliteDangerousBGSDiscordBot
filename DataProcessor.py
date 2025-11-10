from DataManager import DataManager
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

class DataProcessor:

    def getMinorFactionSystemsRecap(guild_id: str):
        systemNames = DataManager.getSystemNamesList(guild_id)
        minorFactionName = DataManager.getMinorFactionName(guild_id)
        minorFactionSystemsRecap = {}

        for systemName in systemNames:
            minorFactionSystemsRecap[systemName] = DataProcessor.getMinorFactionSystemRecap(guild_id, systemName, minorFactionName)

        return minorFactionSystemsRecap
        

    def getMinorFactionSystemRecap(guild_id: str, systemName: str, minorFactionName: str):
        system = DataManager.getSystem(guild_id, systemName)
        return SystemMinorFactionRecap(system, minorFactionName)

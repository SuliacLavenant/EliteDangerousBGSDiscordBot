
from APIRequester.APIManager import APIManager
from DataStorageManager import DataStorageManager

from DataClass.MinorFaction import MinorFaction
from DataClass.System import System

class DataManager:
    #Set tracked minor faction
    def setPlayerMinorFaction(guild_id: str, minorFactionName: str):
        if DataStorageManager.isGuildFileExist(guild_id):
            DataStorageManager.resetDataFile(guild_id)
        else:
            DataStorageManager.createDataFile(guild_id)
        
        minorFaction = APIManager.requestMinorFactionBaseInformation(minorFactionName)
        DataStorageManager.setMinorFactionToDataFile(guild_id,minorFaction)


    def addSystemToIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.addSystemToIgnoreListToDataFile(guild_id, systemName)

    
    def removeSystemFromIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.removeSystemFromIgnoreListFromDataFile(guild_id, systemName)


    #fetch systems data from APIs
    def fetchSystemsData(guild_id: str):
        minorFactionName = DataStorageManager.getMinorFactionName(guild_id)
        systemsNames = APIManager.requestMinorFactionSystemsList(minorFactionName)

        for systemName in systemsNames:
            DataManager.fetchSystemData(guild_id, systemName)


    #fetch system data from API
    def fetchSystemData(guild_id: str, systemName: str):
        system = APIManager.requestSystemData(systemName)
        system = APIManager.requestMinorFactionSystemData(system)
        DataStorageManager.addSystemToDataFile(guild_id,system)

    ############################
    ############################ GET
    ############################

    def getMinorFactionName(guild_id: str):
        return DataStorageManager.getMinorFactionName(guild_id)
    
    #get the systems list from storage
    def getSystemNamesList(guild_id: str):
        return DataStorageManager.getSystemNamesList(guild_id)
    
    #get the system from storage
    def getSystem(guild_id: str, systemName: str):
        return DataStorageManager.getSystem(guild_id, systemName)

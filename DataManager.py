
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
        
        if minorFaction == None:
            print("no minor faction found")
            return False
        else:
            DataStorageManager.setMinorFactionToDataFile(guild_id,minorFaction)
            return True


    def addSystemToIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.addSystemToIgnoreListToDataFile(guild_id, systemName)

    
    def removeSystemFromIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.removeSystemFromIgnoreListFromDataFile(guild_id, systemName)

    ############################
    ############################ API Request
    ############################

    #request system names list from APIs
    def requestSystemNamesList(minorFactionName: str):
        return APIManager.requestMinorFactionSystemsList(minorFactionName)

    #request systems data from APIs
    def requestAndStoreSystemsData(guild_id: str):
        minorFactionName = DataStorageManager.getMinorFactionName(guild_id)
        systems = DataManager.requestSystemsData(minorFactionName)
        for system in systems:
            DataStorageManager.addSystemToDataFile(guild_id,system)
        return True

    #request systems data from APIs
    def requestSystemsData(minorFactionName: str):
        systems = []
        for systemName in DataManager.requestSystemNamesList(minorFactionName):
            systems.append(DataManager.requestSystemData(systemName))
        return systems

    #request system data from API
    def requestSystemData(systemName: str):
        system = APIManager.requestSystemData(systemName)
        system = APIManager.requestMinorFactionSystemData(system)
        return system


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



    ############################ UPDATE
    def updateSystemsData(guild_id: str):
        pass

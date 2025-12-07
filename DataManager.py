
from APIRequester.APIManager import APIManager
from DataStorageManager import DataStorageManager

from DataClass.MinorFaction import MinorFaction
from DataClass.System import System
from DataClass.SystemGroup import SystemGroup


class DataManager:
    def initStorage(guild_id: str):
        if DataStorageManager.isGuildFileExist(guild_id):
            return False
        else:
            DataStorageManager.createDataFile(guild_id)
            return True
        

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
            DataStorageManager.storeMinorFaction(guild_id,minorFaction)
            return True


    def addSystemToIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.addSystemToIgnoreListToDataFile(guild_id, systemName)

    
    def removeSystemFromIgnoreList(guild_id: str, systemName: str):
        DataStorageManager.removeSystemFromIgnoreListFromDataFile(guild_id, systemName)

    def saveSystemGroup(guild_id: str, systemGroup: SystemGroup):
        DataStorageManager.storeSystemGroup(guild_id, systemGroup)

    def removeSystemGroup(guild_id: str, systemGroupName: str):
        DataStorageManager.removeSystemGroup(guild_id, systemGroupName)

    ############################
    ############################ API Request
    ############################

    #request system names list from APIs
    def requestSystemNamesList(minorFactionName: str):
        return APIManager.requestMinorFactionSystemsList(minorFactionName)

    #request systems data from APIs
    def requestAndStoreSystemsData(guild_id: str):
        minorFactionName = DataManager.getMinorFactionName(guild_id)
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

    #request system data from API
    def requestAndStoreSystemData(guild_id: str, systemName: str):
        system = DataManager.requestSystemData(systemName)
        DataStorageManager.addSystemToDataFile(guild_id, system)
        return True


    ############################
    ############################ GET
    ############################

    def getMinorFaction(guild_id: str):
        return DataStorageManager.getMinorFaction(guild_id)

    def getMinorFactionName(guild_id: str):
        minorFaction = DataStorageManager.getMinorFaction(guild_id)
        if minorFaction!=None:
            return minorFaction.name
        else:
            return ""

    #get the systems list from storage
    def getSystemNamesList(guild_id: str):
        return DataStorageManager.getSystemNamesList(guild_id)
    
    #get the system from storage
    def getSystem(guild_id: str, systemName: str):
        return DataStorageManager.getSystem(guild_id, systemName)

    def getSystemGroups(guild_id: str):
        return DataStorageManager.getSystemGroups(guild_id)

    def getSystemGroup(guild_id: str, systemGroupName: str):
        return DataStorageManager.getSystemGroup(guild_id, systemGroupName)

    def getSystemNamesWithNoGroupList(guild_id: str):
        systemNames = DataManager.getSystemNamesList(guild_id)
        systemGroups = DataManager.getSystemGroups(guild_id)
        for systemGroup in systemGroups:
            for systemName in systemNames[:]:
                if systemGroup.haveSystem(systemName):
                    systemNames.remove(systemName)
        return systemNames

    ############################ UPDATE
    def updateSystemsData(guild_id: str):
        pass

    def updateSystemsBGSData(guild_id: str):
        storedSystemNamesList = DataStorageManager.getSystemNamesList(guild_id)
        if storedSystemNamesList==None:
            return False
        elif len(storedSystemNamesList)==0:
            DataManager.requestAndStoreSystemsData(guild_id)
            return True
        else:
            minorFactionName = DataManager.getMinorFactionName(guild_id)
            apiSystemNamesList = DataManager.requestSystemNamesList(minorFactionName)

            if apiSystemNamesList != None:
                # remove lost systems
                for systemName in (set(storedSystemNamesList)-set(apiSystemNamesList)):
                    DataStorageManager.removeSystemFromDataFile(guild_id,systemName)

                # add aquiered systems
                for systemName in (set(apiSystemNamesList)-set(storedSystemNamesList)):
                    DataManager.requestAndStoreSystemData(guild_id,systemName)

            # update the other systems
            storedSystemNamesList = DataStorageManager.getSystemNamesList(guild_id)
            for systemName in storedSystemNamesList:
                print(systemName)
                DataManager.updateSystemBGSData(guild_id, systemName)
            
            return True


    def updateSystemBGSData(guild_id: str, systemName: str):
        system = DataManager.requestSystemData(systemName)
        return DataStorageManager.updateSystemFactions(guild_id, system)

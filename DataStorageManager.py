import os
import shutil
import json

from BotConfig import BotConfig

from DataClass.MinorFaction import MinorFaction
from DataClass.System import System
from DataClass.SystemGroup import SystemGroup

#TODO refaire proprement avec des catch
class DataStorageManager:

    def readFileContent(filePath: str):
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            return {}
    
    def atomicWriteFileContent(filePath: str, data: dict):
        with open(filePath+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(filePath+".tmp", filePath)


    def getGuildFolderPath(guild_id: str):
        return f"{BotConfig.guildsDataFolder}/{guild_id}/"

    def initDataFiles(guild_id: str):
        guildFolderPath = DataStorageManager.getGuildFolderPath(guild_id)
        templateFolderPath = DataStorageManager.getGuildFolderPath("template")

        #create guild data folder if not exist
        if not os.path.exists(guildFolderPath):
            os.makedirs(guildFolderPath)

        #copy requiered files
        fileNames = ["minorFaction.json","systems.json","systemGroups.json"]
        for fileName in fileNames:
            shutil.copy(templateFolderPath+fileName,guildFolderPath+fileName)
            print(fileName)


##################################################
################################################## Minor Faction

    #set minor faction to the data file
    def storeMinorFaction(guild_id: str, minorFaction: MinorFaction):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"minorFaction.json"
        minorFactionData = DataStorageManager.readFileContent(filePath)

        #data update
        minorFactionData["name"] = minorFaction.name
        minorFactionData["allegiance"] = minorFaction.allegiance
        minorFactionData["government"] = minorFaction.government
        DataStorageManager.atomicWriteFileContent(filePath,minorFactionData)
        return True


    def getMinorFaction(guild_id: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"minorFaction.json"
        minorFactionData = DataStorageManager.readFileContent(filePath)

        if minorFactionData!=None and minorFactionData["name"]!= "":
            minorFaction = MinorFaction.initFromStoredData(minorFactionData)
            return minorFaction
        else:
            return None


##################################################
################################################## Systems

    def addSystemToDataFile(guild_id: str, system: System):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.readFileContent(filePath)

        systemsData[system.name] = {}
        systemsData[system.name]["name"] = system.name
        systemsData[system.name]["population"] = system.population
        systemsData[system.name]["security"] = system.security
        systemsData[system.name]["economy"] = system.economy
        systemsData[system.name]["secondEconomy"] = system.secondEconomy
        systemsData[system.name]["reserve"] = system.reserve
        systemsData[system.name]["controllingFaction"] = system.controllingFaction
        systemsData[system.name]["factions"] = system.factions

        DataStorageManager.atomicWriteFileContent(filePath,systemsData)
        return True


    def removeSystemFromDataFile(guild_id: str, systemName: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.readFileContent(filePath)

        #data update
        if systemName in systemsData:
            del systemsData[systemName]

        DataStorageManager.atomicWriteFileContent(filePath,systemsData)
        return True


    def getSystemNamesList(guild_id: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.readFileContent(filePath)

        return list(systemsData.keys())


    def getSystem(guild_id: str, systemName: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.readFileContent(filePath)

        if systemName in systemsData:
            system = System.initFromStoredData(systemsData[systemName])
            return system
        else:
            return None


    def updateSystem(guild_id: str, system: System):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.readFileContent(filePath)

        if system.name in systemsData:
            systemsData[system.name]["population"] = system.population
            systemsData[system.name]["security"] = system.security
            systemsData[system.name]["economy"] = system.economy
            systemsData[system.name]["secondEconomy"] = system.secondEconomy
            systemsData[system.name]["reserve"] = system.reserve
            systemsData[system.name]["controllingFaction"] = system.controllingFaction
            systemsData[system.name]["factions"] = system.factions

            DataStorageManager.atomicWriteFileContent(filePath,systemsData)
            return True
        else:
            return False


##################################################
################################################## System Groups

    def storeSystemGroup(guild_id: str, systemGroup: SystemGroup):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.readFileContent(filePath)

        #data update
        systemGroupsData[systemGroup.name] = {}
        systemGroupsData[systemGroup.name]["name"] = systemGroup.name
        systemGroupsData[systemGroup.name]["color"] = systemGroup.color
        systemGroupsData[systemGroup.name]["systems"] = systemGroup.systems

        DataStorageManager.atomicWriteFileContent(filePath,systemGroupsData)
        return True
    
    
    def getSystemGroupNames(guild_id: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.readFileContent(filePath)

        return list(systemGroupsData["systemGroups"].keys())


    def getSystemGroups(guild_id: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.readFileContent(filePath)

        systemGroups = []
        for systemGroupDict in systemGroupsData.values():
            systemGroups.append(SystemGroup.initFromDict(systemGroupDict))

        return systemGroups


    def getSystemGroup(guild_id: str, systemGroupName: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.readFileContent(filePath)

        if systemGroupName in systemGroupsData.keys():
            return SystemGroup.initFromDict(systemGroupsData[systemGroupName])
        else:
            return None


    def removeSystemGroup(guild_id: str, systemGroupName: str):
        filePath = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.readFileContent(filePath)
        
        if systemGroupName in systemGroupsData.keys():
            systemGroupsData.pop(systemGroupName)
            DataStorageManager.atomicWriteFileContent(filePath,systemGroupsData)
            return True
        else:
            return False


##################################################
##################################################

############ To refactor


    def getGuildFilePath(guild_id: str):
        return f"{BotConfig.guildsDataFolder}/{guild_id}.json"

    def isGuildFileExist(guild_id: str):
        filePath = DataStorageManager.getGuildFilePath(guild_id)
        return os.path.exists(filePath)

    #create storage file for the discord
    def createDataFile(guild_id: str):
        filePath = DataStorageManager.getGuildFilePath(guild_id)

        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        if not os.path.exists(filePath):
            data = {}
            data["faction"] = {}
            data["systems"] = {}
            data["ignoredSystem"] = []
            data["systemGroups"] = {}
            with open(filePath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("Data file created")
        else:
            print("Data file already exist")
    

    #reset the data file content
    def resetDataFile(guild_id: str):
        filePath = DataStorageManager.getGuildFilePath(guild_id)

        if os.path.exists(filePath):
            with open(filePath, "w", encoding="utf-8") as f:
                f.write("{}")
            print("Data file reset")
        else:
            print("Data file do not exist")


    def addSystemToIgnoreListToDataFile(guild_id: str, systemName: str):
        filePath = DataStorageManager.getGuildFilePath(guild_id)

        #read actual content
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            data = {}

        #data update
        if systemName not in data["ignoredSystem"]:
            data["ignoredSystem"].append(systemName)
        else:
            return False

        #atomic write
        with open(filePath+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(filePath+".tmp", filePath)

        return True

    def removeSystemFromIgnoreListFromDataFile(guild_id: str, systemName: str):
        filePath = DataStorageManager.getGuildFilePath(guild_id)

        #read actual content
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            data = {}

        #data update
        
        if systemName in data["ignoredSystem"]:
            data["ignoredSystem"].remove(systemName)
        else:
            return False

        #atomic write
        with open(filePath+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(filePath+".tmp", filePath)

        return True



    ############################################# GET



        
######################### Group


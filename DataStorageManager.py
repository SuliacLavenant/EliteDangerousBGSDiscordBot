import os
import shutil
import json

from BotConfig.BotConfig import BotConfig

from DataClass.DiplomaticSystem import DiplomaticSystem
from DataClass.MinorFaction import MinorFaction
from DataClass.System import System
from DataClass.SystemGroup import SystemGroup
from DataClass.GuildSettings import GuildSettings

#TODO refaire proprement avec des catch
class DataStorageManager:
    files_name: list = ["guildSettings.json","minorFactions.json","systems.json","systemGroups.json","diplomaticSystems.json","players.json","squadrons.json"]

    def read_file_content(file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {type(e).__name__}")
            return {}
    
    def atomic_write_file_content(file_path: str, data: dict):
        with open(file_path+".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(file_path+".tmp", file_path)


    def getGuildFolderPath(guild_id: str):
        return f"{BotConfig.guildsDataFolder}/{guild_id}/"


    def create_missing_data_files(guild_id: str):
        guild_folder_path = DataStorageManager.getGuildFolderPath(guild_id)
        template_folder_path = DataStorageManager.getGuildFolderPath("template")

        #create guild data folder if not exist
        if not os.path.exists(guild_folder_path):
            os.makedirs(guild_folder_path)

        #copy requiered files
        for file_name in DataStorageManager.files_name:
            if not os.path.exists(guild_folder_path+file_name):
                shutil.copy(template_folder_path+file_name,guild_folder_path+file_name)


##################################################
################################################## Minor Faction

    #set minor faction to the data file
    def storeMinorFaction(guild_id: str, minorFaction: MinorFaction):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"minorFaction.json"
        minorFactionsData = DataStorageManager.read_file_content(file_path)

        #data update
        minorFactionsData[minorFaction.name] = {}
        minorFactionsData[minorFaction.name]["name"] = minorFaction.name
        minorFactionsData[minorFaction.name]["allegiance"] = minorFaction.allegiance
        minorFactionsData[minorFaction.name]["government"] = minorFaction.government
        minorFactionsData[minorFaction.name]["originSystemName"] = minorFaction.originSystemName
        DataStorageManager.atomic_write_file_content(file_path,minorFactionsData)
        return True


    def get_minor_faction(guild_id: str, minor_faction_name: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"minorFaction.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)

        if minor_faction_name in minor_factions_data.keys():
            minor_faction = MinorFaction.initFromStoredData(minor_factions_data[minor_faction_name])
            return minor_faction
        else:
            return None


##################################################
################################################## Systems

    def addSystemToDataFile(guild_id: str, system: System):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.read_file_content(file_path)

        systemsData[system.name] = {}
        systemsData[system.name]["name"] = system.name
        systemsData[system.name]["population"] = system.population
        systemsData[system.name]["security"] = system.security
        systemsData[system.name]["economy"] = system.economy
        systemsData[system.name]["secondEconomy"] = system.secondEconomy
        systemsData[system.name]["reserve"] = system.reserve
        systemsData[system.name]["controllingFactionName"] = system.controllingFactionName
        systemsData[system.name]["factions"] = system.factions
        systemsData[system.name]["isOrigin"] = system.isOrigin
        systemsData[system.name]["isArchitected"] = system.isArchitected
        systemsData[system.name]["architect"] = system.architect
        systemsData[system.name]["isDiplomatic"] = system.isDiplomatic
        systemsData[system.name]["lastInfluenceUpdate"] = system.lastInfluenceUpdate

        DataStorageManager.atomic_write_file_content(file_path,systemsData)
        return True


    def removeSystemFromDataFile(guild_id: str, systemName: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.read_file_content(file_path)

        #data update
        if systemName in systemsData:
            del systemsData[systemName]

        DataStorageManager.atomic_write_file_content(file_path,systemsData)
        return True


    def get_system_names_list(guild_id: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)

        return list(systems_data.keys())


    def get_system(guild_id: str, system_name: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)

        if system_name in systems_data:
            system = System.initFromStoredData(systems_data[system_name])
            return system
        else:
            return None


    def updateSystem(guild_id: str, system: System):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.read_file_content(file_path)

        if system.name in systemsData:
            systemsData[system.name]["population"] = system.population
            systemsData[system.name]["security"] = system.security
            systemsData[system.name]["economy"] = system.economy
            systemsData[system.name]["secondEconomy"] = system.secondEconomy
            systemsData[system.name]["reserve"] = system.reserve
            systemsData[system.name]["controllingFactionName"] = system.controllingFactionName
            systemsData[system.name]["factions"] = system.factions
            systemsData[system.name]["isOrigin"] = system.isOrigin
            systemsData[system.name]["isArchitected"] = system.isArchitected
            systemsData[system.name]["architect"] = system.architect
            systemsData[system.name]["isDiplomatic"] = system.isDiplomatic
            systemsData[system.name]["lastInfluenceUpdate"] = system.lastInfluenceUpdate

            DataStorageManager.atomic_write_file_content(file_path,systemsData)
            return True
        else:
            return False


    def updateSystems(guild_id: str, systems: list):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systems.json"
        systemsData = DataStorageManager.read_file_content(file_path)

        for system in systems:
            if system.name in systemsData:
                systemsData[system.name]["population"] = system.population
                systemsData[system.name]["security"] = system.security
                systemsData[system.name]["economy"] = system.economy
                systemsData[system.name]["secondEconomy"] = system.secondEconomy
                systemsData[system.name]["reserve"] = system.reserve
                systemsData[system.name]["controllingFactionName"] = system.controllingFactionName
                systemsData[system.name]["factions"] = system.factions
                systemsData[system.name]["isOrigin"] = system.isOrigin
                systemsData[system.name]["isArchitected"] = system.isArchitected
                systemsData[system.name]["architect"] = system.architect
                systemsData[system.name]["isDiplomatic"] = system.isDiplomatic
                systemsData[system.name]["lastInfluenceUpdate"] = system.lastInfluenceUpdate
            else:
                print(f"{system.name} do not exist in storage")

        DataStorageManager.atomic_write_file_content(file_path,systemsData)
        return True


##################################################
################################################## System Groups

    def storeSystemGroup(guild_id: str, system_group: SystemGroup):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        system_groups_dict[system_group.name] = system_group.get_as_dict()

        DataStorageManager.atomic_write_file_content(file_path,system_groups_dict)
        return True

    
    def getSystemGroupNames(guild_id: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        return list(system_groups_dict.keys())


    def get_system_groups(guild_id: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        system_groups = []
        for system_group_dict in system_groups_dict.values():
            system_groups.append(SystemGroup.init_from_dict(system_group_dict))

        return system_groups


    def get_system_group(guild_id: str, system_group_name: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        if system_group_name in system_groups_dict.keys():
            return SystemGroup.init_from_dict(system_groups_dict[system_group_name])
        else:
            return None


    def removeSystemGroup(guild_id: str, systemGroupName: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"systemGroups.json"
        systemGroupsData = DataStorageManager.read_file_content(file_path)
        
        if systemGroupName in systemGroupsData.keys():
            systemGroupsData.pop(systemGroupName)
            DataStorageManager.atomic_write_file_content(file_path,systemGroupsData)
            return True
        else:
            return False


##################################################
################################################## Guild Settings

    def get_guild_settings(guild_id: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"guildSettings.json"
        guild_settings_dict = DataStorageManager.read_file_content(file_path)
        return GuildSettings.init_from_dict(guild_settings_dict)


    def store_guild_settings(guild_id: str, guild_settings: GuildSettings):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"guildSettings.json"
        DataStorageManager.atomic_write_file_content(file_path,guild_settings.get_as_dict())
        return True


##################################################
##################################################


######################## Diplomatic System

    def storeDiplomaticSystem(guild_id: str, diplomaticSystem: DiplomaticSystem):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        #data update
        diplomaticSystemsData[diplomaticSystem.systemName] = {}
        diplomaticSystemsData[diplomaticSystem.systemName]["systemName"] = diplomaticSystem.systemName
        diplomaticSystemsData[diplomaticSystem.systemName]["diplomaticPositions"] = diplomaticSystem.diplomaticPositions
        diplomaticSystemsData[diplomaticSystem.systemName]["description"] = diplomaticSystem.description

        DataStorageManager.atomic_write_file_content(file_path,diplomaticSystemsData)

        #notify the system that it have diplomatic
        system = DataStorageManager.get_system(guild_id,diplomaticSystem.systemName)
        if system != None:
            system.isDiplomatic = True
            DataStorageManager.updateSystem(guild_id,system)

        return True


    def getDiplomaticSystemNames(guild_id: str):############
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        return list(diplomaticSystemsData.keys())


    def getDiplomaticSystems(guild_id: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        diplomaticSystems = []
        for diplomaticSystemDict in diplomaticSystemsData.values():
            diplomaticSystems.append(DiplomaticSystem.initFromStoredData(diplomaticSystemDict))

        return diplomaticSystems


    def getDiplomaticSystem(guild_id: str, diplomaticSystemName: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        if diplomaticSystemName in diplomaticSystemsData.keys():
            return DiplomaticSystem.initFromStoredData(diplomaticSystemsData[diplomaticSystemName])
        else:
            return None


    def removeDiplomaticSystem(guild_id: str, diplomaticSystemName: str):
        file_path = DataStorageManager.getGuildFolderPath(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)
        
        if diplomaticSystemName in diplomaticSystemsData.keys():
            diplomaticSystemsData.pop(diplomaticSystemName)
            DataStorageManager.atomic_write_file_content(file_path,diplomaticSystemsData)

            #notify the system that it is no more diplomatic
            system = DataStorageManager.get_system(guild_id,diplomaticSystemName)
            if system != None:
                system.isDiplomatic = False
                DataStorageManager.updateSystem(guild_id,system)

            return True
        else:
            return False

        
######################### Diplomatic System


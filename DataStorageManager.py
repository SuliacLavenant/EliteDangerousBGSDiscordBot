import os
import shutil
import json

from BotConfig.BotConfig import BotConfig

from DataClass.DiplomaticSystem import DiplomaticSystem
from DataClass.MinorFaction import MinorFaction
from DataClass.Mission.Mission import Mission
from DataClass.Mission.SystemMission.RetreatMinorFactionFromSystemMission import RetreatMinorFactionFromSystemMission
from DataClass.Mission.SystemMission.SetMinorFactionAsLeaderInSystemMission import SetMinorFactionAsLeaderInSystemMission
from DataClass.System import System
from DataClass.SystemGroup import SystemGroup
from DataClass.GuildSettings import GuildSettings

#TODO refaire proprement avec des catch
class DataStorageManager:
    files_name: list = ["guildSettings.json","minorFactions.json","missions.json","systems.json","systemGroups.json","diplomaticSystems.json","players.json","squadrons.json"]

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


    def get_guild_folder_path(guild_id: str):
        return f"{BotConfig.guildsDataFolder}/{guild_id}/"


    def create_missing_data_files(guild_id: str):
        guild_folder_path = DataStorageManager.get_guild_folder_path(guild_id)
        template_folder_path = DataStorageManager.get_guild_folder_path("template")

        #create guild data folder if not exist
        if not os.path.exists(guild_folder_path):
            os.makedirs(guild_folder_path)

        #copy requiered files
        for file_name in DataStorageManager.files_name:
            if not os.path.exists(guild_folder_path+file_name):
                shutil.copy(template_folder_path+file_name,guild_folder_path+file_name)


##################################################
################################################## Minor Faction


    def store_minor_faction(guild_id: str, minor_faction: MinorFaction):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)
        minor_factions_data[minor_faction.name.lower()] = minor_faction.get_as_dict()
        
        DataStorageManager.atomic_write_file_content(file_path,minor_factions_data)
        return True


    def store_minor_factions(guild_id: str, minor_factions: list):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)
        for minor_faction in minor_factions:
            minor_factions_data[minor_faction.name.lower()] = minor_faction.get_as_dict()
        
        DataStorageManager.atomic_write_file_content(file_path,minor_factions_data)
        return True

    def store_minor_factions_dict(guild_id: str, minor_factions_dict: dict):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)
        for minor_faction_name in minor_factions_dict:
            minor_factions_data[minor_faction_name] = minor_factions_dict[minor_faction_name].get_as_dict()
        
        DataStorageManager.atomic_write_file_content(file_path,minor_factions_data)
        return True


    def get_minor_faction(guild_id: str, minor_faction_name: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)

        if minor_faction_name in minor_factions_data.keys():
            minor_faction = MinorFaction.init_from_dict(minor_factions_data[minor_faction_name])
            return minor_faction
        else:
            return None


    def get_minor_faction_names(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)
        return minor_factions_data.keys()


    def get_minor_factions(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"minorFactions.json"
        minor_factions_data = DataStorageManager.read_file_content(file_path)

        minor_factions = {}
        for minor_faction_name in minor_factions_data:
            minor_factions[minor_faction_name] = MinorFaction.init_from_dict(minor_factions_data[minor_faction_name])

        return minor_factions


##################################################
################################################## Systems

    def store_system(guild_id: str, system: System):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)
        systems_data[system.name] = system.get_as_dict()

        for minor_faction_name in system.minor_factions:
            minor_faction = system.minor_factions[minor_faction_name]
            minor_faction.add_system(system.name)
            DataStorageManager.store_minor_faction(guild_id,minor_faction)

        DataStorageManager.atomic_write_file_content(file_path,systems_data)
        return True


    def removeSystemFromDataFile(guild_id: str, system_name: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systems.json"
        systemsData = DataStorageManager.read_file_content(file_path)

        #data update
        if system_name in systemsData:
            system = DataStorageManager.get_system(guild_id,system_name)
            for minor_faction in system.minor_factions:
                minor_faction.remove_system(system_name)
            del systemsData[system_name]

        DataStorageManager.atomic_write_file_content(file_path,systemsData)
        DataStorageManager.store_minor_factions(guild_id,system.minor_factions)
        return True


    def get_system_names_list(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)

        return list(systems_data.keys())


    def get_system(guild_id: str, system_name: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)

        if system_name in systems_data:
            system = System.init_from_dict(systems_data[system_name])
            for minor_faction_name in system.minor_factions_names:
                system.minor_factions[minor_faction_name] = DataStorageManager.get_minor_faction(guild_id,minor_faction_name)
            return system
        else:
            return None


    def updateSystems(guild_id: str, systems: list):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systems.json"
        systems_data = DataStorageManager.read_file_content(file_path)
        stored_minor_factions = DataStorageManager.get_minor_factions(guild_id)

        for system in systems:
            if system.name in systems_data:
                systems_data[system.name] = system.get_as_dict()
                for minor_faction_name in system.minor_factions_names:
                    if minor_faction_name not in stored_minor_factions:
                        system.minor_factions[minor_faction_name].add_system(system.name)
                        stored_minor_factions[minor_faction_name] = system.minor_factions[minor_faction_name]
                    elif system.name not in stored_minor_factions[minor_faction_name].system_names:
                        stored_minor_factions[minor_faction_name].add_system(system.name)
            else:
                print(f"{system.name} do not exist in storage")

        DataStorageManager.store_minor_factions_dict(guild_id,stored_minor_factions)
        DataStorageManager.atomic_write_file_content(file_path,systems_data)
        return True


##################################################
################################################## System Groups

    def store_system_group(guild_id: str, system_group: SystemGroup):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        system_groups_dict[system_group.name] = system_group.get_as_dict()

        DataStorageManager.atomic_write_file_content(file_path,system_groups_dict)
        return True

    
    def getSystemGroupNames(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        return list(system_groups_dict.keys())


    def get_system_groups(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        system_groups = []
        for system_group_dict in system_groups_dict.values():
            system_groups.append(SystemGroup.init_from_dict(system_group_dict))

        return system_groups


    def get_system_group(guild_id: str, system_group_name: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)

        if system_group_name in system_groups_dict.keys():
            return SystemGroup.init_from_dict(system_groups_dict[system_group_name])
        else:
            return None


    def rename_system_group(guild_id: str, system_group_name: str, system_group_new_name: str):
        system_group = DataStorageManager.get_system_group(guild_id,system_group_name)

        if system_group != None:
            DataStorageManager.remove_system_group(guild_id,system_group_name)
            system_group.name = system_group_new_name
            return DataStorageManager.store_system_group(guild_id,system_group)
        else:
            return False


    def remove_system_group(guild_id: str, system_group_name: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"systemGroups.json"
        system_groups_dict = DataStorageManager.read_file_content(file_path)
        
        if system_group_name in system_groups_dict.keys():
            system_groups_dict.pop(system_group_name)
            DataStorageManager.atomic_write_file_content(file_path,system_groups_dict)
            return True
        else:
            return False


##################################################
################################################## Guild Settings

    def get_guild_settings(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"guildSettings.json"
        guild_settings_dict = DataStorageManager.read_file_content(file_path)
        return GuildSettings.init_from_dict(guild_settings_dict)


    def store_guild_settings(guild_id: str, guild_settings: GuildSettings):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"guildSettings.json"
        DataStorageManager.atomic_write_file_content(file_path,guild_settings.get_as_dict())
        return True


##################################################
##################################################


######################## Diplomatic System

    def storeDiplomaticSystem(guild_id: str, diplomaticSystem: DiplomaticSystem):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"diplomaticSystems.json"
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
            DataStorageManager.store_system(guild_id,system)

        return True


    def getDiplomaticSystemNames(guild_id: str):############
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        return list(diplomaticSystemsData.keys())


    def getDiplomaticSystems(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        diplomaticSystems = []
        for diplomaticSystemDict in diplomaticSystemsData.values():
            diplomaticSystems.append(DiplomaticSystem.initFromStoredData(diplomaticSystemDict))

        return diplomaticSystems


    def getDiplomaticSystem(guild_id: str, diplomaticSystemName: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)

        if diplomaticSystemName in diplomaticSystemsData.keys():
            return DiplomaticSystem.initFromStoredData(diplomaticSystemsData[diplomaticSystemName])
        else:
            return None


    def removeDiplomaticSystem(guild_id: str, diplomaticSystemName: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"diplomaticSystems.json"
        diplomaticSystemsData = DataStorageManager.read_file_content(file_path)
        
        if diplomaticSystemName in diplomaticSystemsData.keys():
            diplomaticSystemsData.pop(diplomaticSystemName)
            DataStorageManager.atomic_write_file_content(file_path,diplomaticSystemsData)

            #notify the system that it is no more diplomatic
            system = DataStorageManager.get_system(guild_id,diplomaticSystemName)
            if system != None:
                system.isDiplomatic = False
                DataStorageManager.store_system(guild_id,system)

            return True
        else:
            return False

        
######################### Diplomatic System



##################################################
################################################## Missions

    #set minor faction to the data file
    def store_mission(guild_id: str, mission: Mission):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"missions.json"
        missions_data = DataStorageManager.read_file_content(file_path)

        if mission.mission_id == None:
            keys = missions_data.keys()
            if len(keys) == 0:
                mission.mission_id = 0
            else:
                mission.mission_id = int(max(keys))+1

        missions_data[mission.mission_id] = mission.get_as_dict()

        DataStorageManager.atomic_write_file_content(file_path,missions_data)
        return True


    def get_missions(guild_id: str):
        file_path = DataStorageManager.get_guild_folder_path(guild_id)+"missions.json"
        missions_data = DataStorageManager.read_file_content(file_path)

        missions = []
        for key in missions_data.keys():
            match missions_data[key]["mission_type"]:
                case "RetreatMinorFactionFromSystemMission":
                    missions.append(RetreatMinorFactionFromSystemMission.init_from_dict(missions_data[key]))
                case "SetMinorFactionAsLeaderInSystemMission":
                    missions.append(SetMinorFactionAsLeaderInSystemMission.init_from_dict(missions_data[key]))

        return missions
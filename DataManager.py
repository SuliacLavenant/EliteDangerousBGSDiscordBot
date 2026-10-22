
from APIRequester.APIManager import APIManager
# from DataStorageManager import DataStorageManager

# from DataClass.DiplomaticSystem import DiplomaticSystem
from DataClass.MinorFaction import MinorFaction
from DataClass.System import System
from DataClass.SystemMinorFactionDetails import SystemMinorFactionDetails
# from DataClass.SystemGroup import SystemGroup
from DataClass.GuildSettings import GuildSettings
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap
import time


from DatabaseGateway.DatabaseGateway import DatabaseGateway

class DataManager:

    #Set tracked minor faction
    def setPlayerMinorFaction(guild_id: str, minorFactionName: str):
        minorFaction = APIManager.requestMinorFactionBaseInformation(minorFactionName)
        if minorFaction == None:
            print("no minor faction found")
            return False
        else:
            DataStorageManager.store_minor_faction(guild_id,minorFaction)

            guildSettings = DataStorageManager.get_guild_settings(guild_id)
            guildSettings.minor_faction_name = minorFaction.name
            DataStorageManager.store_guild_settings(guild_id,guildSettings)

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
        print("outdated")
        minorFactionName = DataManager.getMinorFactionName(guild_id)
        systems = DataManager.requestSystemsData(minorFactionName)
        for system in systems:
            DataStorageManager.store_system(guild_id,system)
        return True

    #request systems data from APIs
    def requestSystemsData(minorFactionName: str):
        print("outdated")
        systems = []
        for systemName in DataManager.requestSystemNamesList(minorFactionName):
            systems.append(DataManager.requestSystemData(systemName))
        return systems


    #request system data from API
    async def request_system_data(system_name: str) -> System | None: #->>>>>>>>>>>>>>>>>
        # system: System = await DatabaseGateway.system.get_by_name(system_name)
        # if system == None:
        #     system = await APIManager.request_system_data(system_name)
        # if system != None:
        #     system = await APIManager.request_minor_faction_system_data(system)
        return await APIManager.request_system_data(system_name)


    async def request_and_store_system_data(system_name: str) -> System | None:
        system: System = await DataManager.request_system_data(system_name)

        if not await DatabaseGateway.system.exists(system.name):
            system_to_store: System = System(name=system.name)
            await DatabaseGateway.system.add(system_to_store)

        system_stored: System = await DatabaseGateway.system.get_by_name(system.name)
        await DatabaseGateway.system.set_name(system_stored.id, system.name)
        await DatabaseGateway.system.set_population(system_stored.id, system.population)
        await DatabaseGateway.system.set_security(system_stored.id, system.security)
        await DatabaseGateway.system.set_economy(system_stored.id, system.economy)
        await DatabaseGateway.system.set_security(system_stored.id, system.second_economy)
        await DatabaseGateway.system.set_reserve(system_stored.id, system.reserve)
        await DatabaseGateway.system.set_last_update_date_time(system_stored.id, system.last_update)

        #remove previous detyails TODO
        minor_faction_ids: list[int] = []
        for system_minor_faction_details in system.system_minor_faction_details_dict_by_name.values():
            minor_faction: MinorFaction = system_minor_faction_details.minor_faction
            if not await DatabaseGateway.minor_faction.exists(minor_faction.name):
                minor_faction_to_add: MinorFaction = MinorFaction(name=minor_faction.name, allegiance=minor_faction.allegiance, government=minor_faction.government)
                await DatabaseGateway.minor_faction.add(minor_faction_to_add)
            minor_faction_stored: MinorFaction = await DatabaseGateway.minor_faction.get_by_name(minor_faction.name)
            minor_faction_ids.append(minor_faction_stored.id)

            #set controlling faction
            if system.controlling_minor_faction_name is not None and system.controlling_minor_faction_name.lower() == system_minor_faction_details.minor_faction.name.lower():
                await DatabaseGateway.system.set_controlling_minor_faction_id(system_stored.id, minor_faction_stored.id)

            if not await DatabaseGateway.system_minor_faction_details.exists(system_stored.id, minor_faction_stored.id):
                system_minor_faction_details_to_store: SystemMinorFactionDetail = SystemMinorFactionDetails(system_id=system_stored.id, minor_faction_id=minor_faction_stored.id)
                await DatabaseGateway.system_minor_faction_details.add(system_minor_faction_details_to_store)
            await DatabaseGateway.system_minor_faction_details.set_influence(system_stored.id, minor_faction_stored.id, system_minor_faction_details.influence)

        #remove minor faction not present anymore
        system_stored = await DatabaseGateway.system.get_by_name(system.name, True)
        minor_faction_removed:bool = False
        for minor_faction_id in system_stored.system_minor_faction_details_dict.keys():
            if minor_faction_id not in minor_faction_ids:
                await DatabaseGateway.system_minor_faction_details.delete(system_stored.id,minor_faction_id)
                minor_faction_removed = True
        
        if minor_faction_removed:
            system_stored = await DatabaseGateway.system.get_by_name(system.name, True)

        return system_stored


    #old i guess
    #request system data from API
    def requestAndStoreSystemData(guild_id: str, systemName: str):
        system = DataManager.requestSystemData(systemName)
        DataStorageManager.store_system(guild_id, system)
        return True


    ############################
    ############################ GET
    ############################
    def getMinorFaction(guild_id: str, minorFactionName: str):
        return DataStorageManager.get_minor_faction(guild_id, minorFactionName)

    def getGuildMinorFactionName(guild_id: str):
        guildSettings = DataStorageManager.get_guild_settings(guild_id)
        return guildSettings.minor_faction_name

    def get_system_names_with_no_group(guild_id: str):
        systemNames = DataStorageManager.get_system_names_list(guild_id)
        systemGroups = DataStorageManager.get_system_groups(guild_id)
        for systemGroup in systemGroups:
            for systemName in systemNames[:]:
                if systemGroup.haveSystem(systemName):
                    systemNames.remove(systemName)
        return systemNames


##################################################
################################################## UPDATE

    #TODO test when possible (elitebgsapi was down when writed)
    def updateSystemsList(guild_id: str):
        minorFactionName = DataManager.getGuildMinorFactionName(guild_id)
        storedSystemNamesList = DataStorageManager.get_system_names_list(guild_id)
        apiSystemNamesList = DataManager.requestSystemNamesList(minorFactionName)

        if apiSystemNamesList != None:
            # add aquiered systems
            for systemName in (set(apiSystemNamesList)-set(storedSystemNamesList)):
                print(f"Aquiered System \"{systemName}\"")
                DataManager.requestAndStoreSystemData(guild_id,systemName)

        print("Check for new and lost systems: DONE")
        return True


    # "system = await DataManager.request_system_data(system_name.lower())"
    #TODO put back change log
    async def update_systems_bgs_data(guild_id: str): #TODO no use for guild_id
        # minorFactionName = DataManager.getGuildMinorFactionName(guild_id)
        # storedSystemNamesList = DataStorageManager.get_system_names_list(guild_id)
        systems: list[System] = await DatabaseGateway.system.get_all()
        system_events = []
        print(f"Updating {len(systems)} systems")
        i = 0
        for system in systems:
            # system = DataStorageManager.get_system(guild_id, systemName)
            # system_new = DataManager.request_system_data(system.name)
            system_new = await DataManager.request_and_store_system_data(system.name)
            # system_events = system_events + system.diff(system_new,minorFactionName)
            # system.update(system_new)
            # systems.append(system)
            i+=1
            print(f"Updated {i}/{len(systems)} systems ({system.name})")
            time.sleep(1)
        
        # DataStorageManager.updateSystems(guild_id, systems)
        print("update_systems_bgs_data: DONE")

        return system_events
    
    # sqg<ggsq
    async def update_system_bgs_data(system: System):
        system_new = await APIManager.request_system_data(system.name)
        if system_new != None:
            system_new = await APIManager.request_minor_faction_system_data(system_new)
        return system_new



    def updateSystemBGSData(guild_id: str, systemName: str):
        system = DataManager.requestSystemData(systemName)
        return DataStorageManager.store_system(guild_id, system)


    ###
    def setSystemArchitect(guild_id: str, systemName: str, architectName: str):
        system = DataStorageManager.get_system(guild_id, systemName)
        system.architect = architectName.lower()
        system.isArchitected = True
        return DataStorageManager.store_system(guild_id, system)


##################################################
################################################## Recap

    # def get_minor_faction_system_recaps(guild_id: str, minor_faction: MinorFaction) -> dict[str,SystemMinorFactionRecap]:
    #     system_names: list[str] = DataStorageManager.get_system_names_list(guild_id)

    #     minor_faction_system_recaps: dict[str,SystemMinorFactionRecap] = {}
    #     system_name: str
    #     for system_name in system_names:
    #         system_recap: SystemMinorFactionRecap = DataManager.get_minor_faction_system_recap(guild_id, system_name, minor_faction.name)
    #         if system_recap != None:
    #             minor_faction_system_recaps[system_name] = system_recap

    #     return minor_faction_system_recaps


    # def get_minor_faction_system_recap(guild_id: str, system_name: str, minor_faction_name: str, include_untracked: bool = False) -> SystemMinorFactionRecap:
    #     system: System = DataStorageManager.get_system(guild_id, system_name)
    #     if not include_untracked and not system.tracked:
    #         return None
    #     diplomatic_system: DiplomaticSystem = None
    #     if system.isDiplomatic:
    #         diplomatic_system = DataStorageManager.getDiplomaticSystem(guild_id,system_name)

    #     return SystemMinorFactionRecap(system,minor_faction_name,diplomatic_system)


    def get_minor_faction_tracked_system_recaps(tracked_systems: list[DiscordTrackedSystem], minor_faction: MinorFaction) -> dict[str,SystemMinorFactionRecap]:
        minor_faction_system_recaps: dict[str,SystemMinorFactionRecap] = {}
        system_name: str
        for tracked_system in tracked_systems:
            system_recap: SystemMinorFactionRecap = DataManager.get_minor_faction_system_recap(tracked_system.system, minor_faction, tracked_system.system_group)
            if system_recap != None:
                minor_faction_system_recaps[tracked_system.system.name] = system_recap

        return minor_faction_system_recaps


    def get_minor_faction_system_recaps(systems: list[System], minor_faction: MinorFaction) -> dict[str,SystemMinorFactionRecap]:
        minor_faction_system_recaps: dict[str,SystemMinorFactionRecap] = {}
        system_name: str
        for system in systems:
            system_recap: SystemMinorFactionRecap = DataManager.get_minor_faction_system_recap(system, minor_faction)
            if system_recap != None:
                minor_faction_system_recaps[system.name] = system_recap

        return minor_faction_system_recaps


    def get_minor_faction_system_recap(system: System, minor_faction: MinorFaction, system_group: SystemGroup = None) -> SystemMinorFactionRecap:
        diplomatic_system: DiplomaticSystem = None
        # if system.isDiplomatic:
        #     diplomatic_system = DataStorageManager.getDiplomaticSystem(guild_id,system_name)

        return SystemMinorFactionRecap(system, minor_faction, diplomatic_system, system_group)

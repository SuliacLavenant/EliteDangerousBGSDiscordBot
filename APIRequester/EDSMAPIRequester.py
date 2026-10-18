import asyncio
from datetime import datetime, timezone
import requests
import urllib.parse

from APIRequester.AbstractAPIRequester import AbstractAPIRequester
from BotConfig.BotConfig import BotConfig
from DataClass.System import System
from DataClass.MinorFaction import MinorFaction
from DataClass.SystemMinorFactionDetails import SystemMinorFactionDetails

from DatabaseGateway.DatabaseGateway import DatabaseGateway


class EDSMAPIRequester(AbstractAPIRequester):
    def getStatus():
        status = {}
        status["name"] = "EDSM API"

        onlineStatus = EDSMAPIRequester.isAPIOnline()
        if onlineStatus == "Online":
            status["online"] = True
            status["issue"] = None
        else:
            status["online"] = False
            status["issue"] = onlineStatus

        return status


    def isAPIOnline():
        url = f"https://www.edsm.net/api-v1/system?systemName=Sol"

        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error
            jsonData = response.json()

            if jsonData["name"]=="Sol":
                return "Online"
            else:
                return "Error"

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return "Timeout"

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return "HTTP Error"


    @classmethod
    async def request_system_data(cls, system_name: str) -> System | None:
        url = f"https://www.edsm.net/api-v1/system"
        params = {
            #"systemName": urllib.parse.quote(systemName),
            "systemName": system_name,
            "showInformation": 1
        }
        headers = {
            "User-Agent": f"EraEliteBGSBOT/0.1 contact: {BotConfig.contact_email}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status() #detect request error
            jsonData = response.json()
            
            if len(jsonData)==0 or len(jsonData["information"])==0:
                return None

            system: System = await DatabaseGateway.system.get_by_name(system_name, True)
            if system is None:
                system = System(name=jsonData["name"])
                await DatabaseGateway.system.add(system)
                system = await DatabaseGateway.system.get_by_name(system_name, True)

            #### TMP TODO (just to update caps name, to remove later)
            await DatabaseGateway.system.set_name(system.id, jsonData["name"])

            await DatabaseGateway.system.set_population(system.id, cls.get_correct_variable(jsonData["information"],"population"))
            await DatabaseGateway.system.set_security(system.id, cls.get_correct_variable(jsonData["information"],"security"))
            await DatabaseGateway.system.set_economy(system.id, cls.get_correct_variable(jsonData["information"],"economy"))
            await DatabaseGateway.system.set_security(system.id, cls.get_correct_variable(jsonData["information"],"second_economy"))
            await DatabaseGateway.system.set_reserve(system.id, cls.get_correct_variable(jsonData["information"],"reserve"))

            # controlling_faction
            controlling_minor_faction_name = cls.get_correct_variable(jsonData["information"],"faction")
            if controlling_minor_faction_name != None:
                minor_faction = await DatabaseGateway.minor_faction.get_by_name(controlling_minor_faction_name)
                if minor_faction != None:
                    await DatabaseGateway.system.set_controlling_minor_faction_id(system.id, minor_faction.id)

            system = await DatabaseGateway.system.get_by_name(system_name,True)
            if system.controlling_minor_faction_id == None and controlling_minor_faction_name != None:
                system.controlling_minor_faction_name = controlling_minor_faction_name

            return system


        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None


    #TODO probleme il ecrase direct la base de donné
    @classmethod
    async def request_minor_faction_system_data(cls, system: System) -> System | None:
        system_id = system.id
        url = f"https://www.edsm.net/api-system-v1/factions"
        params = {
            #"systemName": urllib.parse.quote(system.name),
            "systemName": system.name,
            "showHistory": 0
        }

        headers = {
            "User-Agent": f"EraEliteBGSBOT/0.1 contact: {BotConfig.contact_email}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status() #detect request error

            timeStampSaved = False

            jsonData = response.json()

            for faction in jsonData["factions"]:
                if faction["influence"]!=0:
                    pendingStates = []
                    activeStates = []
                    recoveringStates = []
                    for state in faction["pendingStates"]:
                        pendingStates.append(state["state"].lower())
                    for state in faction["activeStates"]:
                        activeStates.append(state["state"].lower())
                    if faction["state"].lower()!= "none" and faction["state"].lower() not in activeStates:
                        activeStates.append(faction["state"].lower())
                    for state in faction["recoveringStates"]:
                        recoveringStates.append(state["state"].lower())

                    minor_faction = await DatabaseGateway.minor_faction.get_by_name(faction["name"])
                    if minor_faction == None:
                        minor_faction = MinorFaction(name=faction["name"], allegiance=faction["allegiance"], government=faction["government"])
                        await DatabaseGateway.minor_faction.add(minor_faction)
                        minor_faction = await DatabaseGateway.minor_faction.get_by_name(faction["name"])

                        if system.controlling_minor_faction_id == None and faction["name"] == system.controlling_faction_name:
                            await DatabaseGateway.system.set_controlling_minor_faction_id(system.id,minor_faction.id)
                    else: # TODO to remove later, it's just to update names     
                        await DatabaseGateway.minor_faction.set_name(minor_faction.id, faction["name"])

                    # create data for minorfaction instance in system
                    if not await DatabaseGateway.system_minor_faction_details.exists(system_id, minor_faction.id):
                        system_minor_faction_details: SystemMinorFactionDetail = SystemMinorFactionDetails(system_id=system_id, minor_faction_id=minor_faction.id)
                        await DatabaseGateway.system_minor_faction_details.add(system_minor_faction_details)
                    
                    # add influence
                    await DatabaseGateway.system_minor_faction_details.set_influence(system_id, minor_faction.id, faction["influence"])


                    if not timeStampSaved: #TODO le mettre en set au datagateaway
                        last_update = datetime.fromtimestamp(faction["lastUpdate"], tz=timezone.utc)
                        await DatabaseGateway.system.set_last_update_date_time(system.id, last_update)
                        timeStampSaved = True


            #TODO check, pas besoin de recuperer la version actuelle pour repartir d'elle vu l'architecture actuelle (set_...)
            return system

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None

import requests
import urllib.parse

# Custom Class
from APIRequester.AbstractAPIRequester import AbstractAPIRequester

from DataClass.System import System
from DataClass.MinorFaction import MinorFaction



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


    def requestSystemData(systemName: str):
        url = f"https://www.edsm.net/api-v1/system?systemName={urllib.parse.quote(systemName)}&showInformation=1"

        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error

            jsonData = response.json()

            secondEconomy = "none"
            if "secondEconomy" in jsonData["information"]:
                secondEconomy = jsonData["information"]["secondEconomy"]

            system = System(name=jsonData["name"], population=jsonData["information"]["population"], security=jsonData["information"]["security"], economy=jsonData["information"]["economy"], secondEconomy=secondEconomy, reserve=jsonData["information"]["reserve"], controllingFaction=jsonData["information"]["faction"])
            return system

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None


    def requestMinorFactionSystemData(system: System):
        url = f"https://www.edsm.net/api-system-v1/factions?systemName={urllib.parse.quote(system.name)}"

        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error

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

                    system.addFaction(faction["name"], faction["allegiance"], faction["government"], faction["influence"], pendingStates, activeStates, recoveringStates)

            return system

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None
import requests
import urllib.parse

# Custom Class
from APIRequester.AbstractAPIRequester import AbstractAPIRequester

from DataClass.System import System
from DataClass.MinorFaction import MinorFaction



class EDSMAPIRequester(AbstractAPIRequester):

    def requestSystemData(systemName: str):
        url = f"https://www.edsm.net/api-v1/system?systemName={urllib.parse.quote(systemName)}&showInformation=1"

        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error

            jsonData = response.json()

            secondEconomy = "none"
            if "secondEconomy" in jsonData["information"]:
                secondEconomy = jsonData["information"]["secondEconomy"]

            system = System(jsonData["name"], jsonData["information"]["population"], jsonData["information"]["security"], jsonData["information"]["economy"], secondEconomy, jsonData["information"]["reserve"], jsonData["information"]["faction"])
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
                    system.addFaction(faction["name"], faction["allegiance"], faction["government"], faction["influence"], faction["state"])

            return system

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None
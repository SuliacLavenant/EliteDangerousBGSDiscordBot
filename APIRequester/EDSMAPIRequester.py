import requests
import urllib.parse

# Custom Class
from APIRequester.AbstractAPIRequester import AbstractAPIRequester

from DataClass.System import System
from DataClass.MinorFaction import MinorFaction



class EDSMAPIRequester(AbstractAPIRequester):

    def requestSystemData(systemName: str):

        jsonData = requests.get(f"https://www.edsm.net/api-v1/system?systemName={urllib.parse.quote(systemName)}&showInformation=1").json()

        system = System(jsonData["name"], jsonData["information"]["population"], jsonData["information"]["security"], jsonData["information"]["economy"], jsonData["information"]["secondEconomy"], jsonData["information"]["reserve"], jsonData["information"]["faction"])

        return system

    def requestMinorFactionSystemData(system: System):
        jsonData = requests.get(f"https://www.edsm.net/api-system-v1/factions?systemName={urllib.parse.quote(system.name)}").json()

        for faction in jsonData["factions"]:
            if faction["influence"]!=0:
                system.addFaction(faction["name"], faction["allegiance"], faction["government"], faction["influence"], faction["state"])


        return system
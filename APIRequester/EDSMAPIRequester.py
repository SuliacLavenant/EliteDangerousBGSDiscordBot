import requests
import urllib.parse

# Custom Class
from APIRequester.AbstractAPIRequester import AbstractAPIRequester

from DataClass.System import System
from DataClass.MinorFaction import MinorFaction



class EDSMAPIRequester(AbstractAPIRequester):

    def requestSystemData(systemName: str):

        jsonData = requests.get(f"https://www.edsm.net/api-v1/system?systemName={urllib.parse.quote(systemName)}&showInformation=1").json()
        print(jsonData)

        system = System(jsonData["name"].lower(), jsonData["information"]["population"], jsonData["information"]["faction"].lower())

        return system

#jsonData = requests.get(f"https://www.edsm.net/api-system-v1/factions?systemName={urllib.parse.quote(systemName)}").json()
import requests
import urllib.parse

# Custom Class
from APIRequester.AbstractAPIRequester import AbstractAPIRequester

from DataClass.System import System
from DataClass.MinorFaction import MinorFaction

from SystemInfoMinorFactionFocused import SystemInfoMinorFactionFocused


class EliteBGSAPIAPIRequester(AbstractAPIRequester):

    def requestMinorFactionBaseInformation(minorFactionName: str):
        url = f"https://elitebgs.app/api/ebgs/v5/factions?name={urllib.parse.quote(minorFactionName)}&minimal=true&systemDetails=false"

        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error

            jsonData = response.json()

            docs = jsonData.get("docs", [])
            if not docs: #no "docs" or empty "docs"
                return None

            return MinorFaction(jsonData["docs"][0]["name_lower"], jsonData["docs"][0]["allegiance"], jsonData["docs"][0]["government"])

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None

        except Exception as e:
            print(f"Error: Invalid API response: {e}")
            return None


    def requestMinorFactionSystemsList(minorFactionName: str):
        systems=[]
        page=1
        pageToRead = True

        while pageToRead:
            jsonData = EliteBGSAPIAPIRequester.requestToApi(f"https://elitebgs.app/api/ebgs/v5/systems?faction={minorFactionName}&minimal=true&factionDetails=false&factionHistory=false&page={page}")

            for s in jsonData["docs"]:
                systems.append(s["name_lower"])

            pageToRead = jsonData["nextPage"]!=None
            page+=1

        return systems
        


    def requestSystemFactionData(systemName: str, minorFactionName: str):

        jsonData = requests.get(f"https://elitebgs.app/api/ebgs/v5/systems?name={systemName}&factionDetails=true").json()

        systemInfoMinorFaction = SystemInfoMinorFactionFocused(jsonData["docs"][0]["name"], minorFactionName)
        systemInfoMinorFaction.setControllingFaction(jsonData["docs"][0]["controlling_minor_faction_cased"])
        
        factionInSystem = False
        otherInfluences = []

        for faction in jsonData["docs"][0]["factions"]:
            if faction["name"] == minorFactionName:
                systemInfoMinorFaction.influence = faction["faction_details"]["faction_presence"]["influence"]
                factionInSystem = True
                if minorFactionName == systemInfoMinorFaction.controllingFaction:
                    systemInfoMinorFaction.controllingFactionInfluence = faction["faction_details"]["faction_presence"]["influence"]
            elif faction["name"] == systemInfoMinorFaction.controllingFaction:
                systemInfoMinorFaction.controllingFactionInfluence = faction["faction_details"]["faction_presence"]["influence"]
                otherInfluences.append(faction["faction_details"]["faction_presence"]["influence"])
            else:
                otherInfluences.append(faction["faction_details"]["faction_presence"]["influence"])
        
        if minorFactionName == systemInfoMinorFaction.controllingFaction:
            systemInfoMinorFaction.positionInSystem = 0
        elif(factionInSystem):
            systemInfoMinorFaction.positionInSystem = 0
            for otherInfluence in otherInfluences:
                if otherInfluence > systemInfoMinorFaction.influence:
                    systemInfoMinorFaction.positionInSystem += 1

        systemInfoMinorFaction.setDate(jsonData["docs"][0]["updated_at"])
        systemInfoMinorFaction.setPopulation(jsonData["docs"][0]["population"])
        
        return systemInfoMinorFaction

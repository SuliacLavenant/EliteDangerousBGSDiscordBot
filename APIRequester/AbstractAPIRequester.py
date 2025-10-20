from abc import ABC, abstractmethod
import requests
import urllib.parse

# Custom Class
from DataClass.System import System
from DataClass.MinorFaction import MinorFaction

class AbstractAPIRequester(ABC):
    @abstractmethod
    def requestMinorFactionSystemsList(minorFactionName: str):
        pass
    @abstractmethod
    def requestSystemFactionData(systemName: str, minorFactionName: str):
        pass

    
    def requestToApi(url: str):
        try:
            response = requests.get(url, timeout=10) #timeout 10 sec
            response.raise_for_status() #detect request error

            jsonData = response.json()

            return jsonData

        except requests.exceptions.Timeout:
            print("Error: Timeout.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: HTTP {e}")
            return None
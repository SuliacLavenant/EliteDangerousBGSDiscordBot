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
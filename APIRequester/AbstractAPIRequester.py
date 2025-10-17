from abc import ABC, abstractmethod
import requests

# Custom Class
from SystemInfoMinorFactionFocused import SystemInfoMinorFactionFocused


class AbstractAPIRequester(ABC):
    @abstractmethod
    def requestMinorFactionSystemsList(minorFactionName: str):
        pass
    @abstractmethod
    def requestSystemFactionData(systemName: str, minorFactionName: str):
        pass
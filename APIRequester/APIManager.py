

from APIRequester.EliteBGSAPIAPIRequester import EliteBGSAPIAPIRequester
from APIRequester.EDSMAPIRequester import EDSMAPIRequester

from DataClass.System import System

# TODO check different api to get the most up to date data
class APIManager:

    def requestSystemData(systemName: str):
        return EDSMAPIRequester.requestSystemData(systemName)

    def requestMinorFactionBaseInformation(minorFactionName: str):
        return EliteBGSAPIAPIRequester.requestMinorFactionBaseInformation(minorFactionName)

    def requestMinorFactionSystemData(system: System):
        return EDSMAPIRequester.requestMinorFactionSystemData(system)

    def requestMinorFactionSystemsList(minorFactionName: str):
        return EliteBGSAPIAPIRequester.requestMinorFactionSystemsList(minorFactionName)
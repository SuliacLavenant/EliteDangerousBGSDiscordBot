from APIRequester.EliteBGSAPIAPIRequester import EliteBGSAPIAPIRequester
from APIRequester.EDSMAPIRequester import EDSMAPIRequester

from DataClass.System import System

# TODO check different api to get the most up to date data
class APIManager:
    def getAPIStatus():
        aPIStatus = {}

        aPIStatus["EliteBGSAPI"] = EliteBGSAPIAPIRequester.getStatus()
        aPIStatus["EDSMAPI"] = EDSMAPIRequester.getStatus()

        return aPIStatus

    async def request_system_data(system_name: str) -> System | None:
        # return await EDSMAPIRequester.request_system_data(system_name)
        return await EDSMAPIRequester.request_system_full_data(system_name)

    def requestMinorFactionBaseInformation(minorFactionName: str):
        return EliteBGSAPIAPIRequester.requestMinorFactionBaseInformation(minorFactionName)

    async def request_minor_faction_system_data(system: System):
        return await EDSMAPIRequester.request_minor_faction_system_data(system)

    def requestMinorFactionSystemsList(minorFactionName: str):
        return EliteBGSAPIAPIRequester.requestMinorFactionSystemsList(minorFactionName)

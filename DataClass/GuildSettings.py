from dataclasses import dataclass, field

@dataclass
class GuildSettings:
    minorFactionName: str = None

    bgsSystemRecapChannelID: int = None
    bgsWarningRecapChannelID: int = None

    #init from Dict
    @classmethod
    def initFromDict(cls, guildSettingsDict: dict):
        guildSettings = cls(
            minorFactionName=guildSettingsDict["minorFactionName"],
            bgsSystemRecapChannelID=guildSettingsDict["bgsSystemRecapChannelID"],
            bgsWarningRecapChannelID=guildSettingsDict["bgsWarningRecapChannelID"]
            )
        return guildSettings

    def getAsDict(self) -> dict:
        guildSettingsDict = {}

        guildSettingsDict["minorFactionName"] = self.minorFactionName

        guildSettingsDict["bgsSystemRecapChannelID"] = self.bgsSystemRecapChannelID
        guildSettingsDict["bgsWarningRecapChannelID"] = self.bgsWarningRecapChannelID

        return guildSettingsDict

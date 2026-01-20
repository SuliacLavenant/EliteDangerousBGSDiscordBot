from dataclasses import dataclass, field

@dataclass
class GuildSettings:
    minorFactionName: str = None

    bgsRecapChanelID: int = None
    bgsWarningRecapChanelID: int = None

    #init from Dict
    @classmethod
    def initFromDict(cls, guildSettingsDict: dict):
        guildSettings = cls(
            minorFactionName=guildSettingsDict["minorFactionName"],
            bgsRecapChanelID=guildSettingsDict["bgsRecapChanelID"],
            bgsWarningRecapChanelID=guildSettingsDict["bgsWarningRecapChanelID"]
            )
        return guildSettings

    def getAsDict(self) -> dict:
        guildSettingsDict = {}

        guildSettingsDict["minorFactionName"] = self.minorFactionName

        guildSettingsDict["bgsRecapChanelID"] = self.bgsRecapChanelID
        guildSettingsDict["bgsWarningRecapChanelID"] = self.bgsWarningRecapChanelID

        return guildSettingsDict

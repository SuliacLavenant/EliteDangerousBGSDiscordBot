from dataclasses import dataclass, field

@dataclass
class GuildSettings:
    bgsRecapChanelID: int = None

    #init from Dict
    @classmethod
    def initFromDict(cls, guildSettingsDict: dict):
        return cls(bgsRecapChanelID=guildSettingsDict["bgsRecapChanelID"])

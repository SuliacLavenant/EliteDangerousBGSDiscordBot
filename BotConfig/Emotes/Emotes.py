from BotConfig.Emotes.SystemInformation import SystemInformation

class Emotes:
    systemInformation: SystemInformation

    def __init__(self, emotesDict: dict):
        self.systemInformation = SystemInformation(emotesDict["systemInformation"])


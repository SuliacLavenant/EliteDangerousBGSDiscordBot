import json

from BotConfig.Emotes.Emotes import Emotes

class BotConfig:
    configPath: str = "config.json"

    guildsDataFolder: str
    leaderInfluenceWarning: dict
    influenceExpansionWarning: float
    influenceRetreatWarning: float

    emotes: dict
    numberOfFactionEmotes: dict
    positionInSystemEmotes: dict
    stateEmotes: dict

    emotesN: Emotes

    @classmethod
    def load(cls):
        with open(cls.configPath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.guildsDataFolder = data["guilds_data_folder"]
        cls.leaderInfluenceWarning = data["systemRecap"]["influenceWarning"]["leader"]
        cls.influenceExpansionWarning = data["systemRecap"]["influenceWarning"]["other"]["expansion"]
        cls.influenceRetreatWarning = data["systemRecap"]["influenceWarning"]["other"]["retreat"]

        # emotes
        cls.emotesN = Emotes(data["emotes"])

        cls.emotes = data["systemRecap"]["emotes"]
        cls.numberOfFactionEmotes = data["systemRecap"]["emotes"]["numberOfFaction"]
        cls.positionInSystemEmotes = data["systemRecap"]["emotes"]["positionInSystem"]

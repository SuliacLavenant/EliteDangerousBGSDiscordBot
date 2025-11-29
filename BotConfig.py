import json

class BotConfig:
    configPath: str = "config.json"

    guildsDataFolder: str
    leaderInfluenceWarning: dict
    influenceRetreatWarning: float
    emotes: dict

    @classmethod
    def load(cls):
        with open(cls.configPath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.guildsDataFolder = data["guilds_data_folder"]
        cls.leaderInfluenceWarning = data["systemRecap"]["influenceWarning"]["leader"]
        cls.influenceRetreatWarning = data["systemRecap"]["influenceWarning"]["other"]["retreat"]
        cls.emotes = data["systemRecap"]["emotes"]


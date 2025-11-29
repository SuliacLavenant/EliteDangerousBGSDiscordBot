import json

class BotConfig:
    configPath: str = "config.json"

    guildsDataFolder: str
    emotes: dict

    @classmethod
    def load(cls):
        with open(cls.configPath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.guildsDataFolder = data["guilds_data_folder"]
        cls.emotes = data["systemRecap"]["emotes"]


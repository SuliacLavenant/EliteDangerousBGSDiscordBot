import json

from BotConfig.Emotes.Emotes import Emotes
from BotConfig.BGS.BGS import BGS

class BotConfig:
    configPath: str = "config.json"

    guildsDataFolder: str
    leaderInfluenceWarning: dict

    emotes: dict
    numberOfFactionEmotes: dict
    positionInSystemEmotes: dict
    stateEmotes: dict

    bgs: BGS
    emotes: Emotes

    indent: str = "⠀"
    indent2: str = "⠀"*2

    @classmethod
    def load(cls):
        with open(cls.configPath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.guildsDataFolder = data["guilds_data_folder"]

        # new
        cls.bgs = BGS(data["bgs"])
        cls.emotes = Emotes(data["emotes"])

from dataclasses import dataclass, field

@dataclass
class Player:
    pseudo: str = ""
    discord_id: int = None
    squadron_tag: str = None


    @classmethod
    def init_from_dict(cls, player_dict: dict):
        player = cls(
            pseudo = player_dict["pseudo"],
            discord_id = player_dict["discord_id"],
            squadron_tag = player_dict["squadron_tag"]
            )
        return player


    def get_as_dict(self) -> dict:
        player_dict = {}
        player_dict["pseudo"] = self.pseudo
        player_dict["discord_id"] = self.discord_id
        player_dict["squadron_tag"] = self.squadron_tag
        return player_dict


    def __str__(self):
        return f"Pseudo: {self.pseudo.title()}"

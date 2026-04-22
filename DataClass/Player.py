from dataclasses import dataclass, field

@dataclass
class Player:
    discord_id: int = None
    id: int = None
    pseudo: str = ""
    squadron_id: str = None


    @classmethod
    def init_from_dict(cls, player_dict: dict):
        player = cls(
            discord_id = player_dict["discord_id"],
            id = player_dict["id"],
            pseudo = player_dict["pseudo"],
            squadron_id = player_dict["squadron_id"]
            )
        return player


    def get_as_dict(self) -> dict:
        player_dict = {}
        player_dict["discord_id"] = self.discord_id
        player_dict["id"] = self.id
        player_dict["pseudo"] = self.pseudo
        player_dict["squadron_id"] = self.squadron_id
        return player_dict


    def __str__(self):
        return f"Pseudo: {self.pseudo.title()}"

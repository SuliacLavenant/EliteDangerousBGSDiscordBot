from dataclasses import dataclass, field

@dataclass
class Player:
    discord_id: int = None
    id: int = None
    name: str = ""
    squadron_id: str = None


    @classmethod
    def init_from_dict(cls, player_dict: dict):
        player = cls(
            discord_id = player_dict["discord_id"],
            id = player_dict["id"],
            name = player_dict["name"],
            squadron_id = player_dict["squadron_id"]
            )
        return player


    def get_as_dict(self) -> dict:
        player_dict = {}
        player_dict["discord_id"] = self.discord_id
        player_dict["id"] = self.id
        player_dict["name"] = self.name
        player_dict["squadron_id"] = self.squadron_id
        return player_dict


    def __str__(self):
        return f"Name: {self.name.title()}"

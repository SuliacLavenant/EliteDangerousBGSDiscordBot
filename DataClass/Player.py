from dataclasses import dataclass, field

@dataclass
class Player:
    architected_systems: list[str] = field(default_factory=list[str])
    discord_id: int = None
    id: int = None
    inara_id: int = None
    name: str = ""
    squadron_id: int = None


    @classmethod
    def init_from_dict(cls, player_dict: dict):
        player = cls(
            architected_systems = player_dict["architected_systems"],
            discord_id = player_dict["discord_id"],
            id = player_dict["id"],
            inara_id = player_dict["inara_id"],
            name = player_dict["name"],
            squadron_id = player_dict["squadron_id"]
            )
        return player


    def get_as_dict(self) -> dict:
        player_dict = {}
        player_dict["architected_systems"] = self.architected_systems
        player_dict["discord_id"] = self.discord_id
        player_dict["id"] = self.id
        player_dict["inara_id"] = self.inara_id
        player_dict["name"] = self.name
        player_dict["squadron_id"] = self.squadron_id
        return player_dict


    def add_architected_system(self, system_name: str) -> bool:
        if system_name.lower() not in self.architected_systems:
            self.architected_systems.append(system_name.lower())
            return True
        else:
            return False


    def __str__(self):
        return f"Name: {self.name.title()}"

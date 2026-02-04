from dataclasses import dataclass, field

@dataclass
class Squadron:
    name: str = ""
    tag: str = ""
    minor_faction_names: list = field(default_factory=list)

    leaders: list = field(default_factory=list)
    officers: list = field(default_factory=list)
    members: list = field(default_factory=list)
    recruits: list = field(default_factory=list)


    @classmethod
    def init_from_dict(cls, squadron_dict: dict):
        squadron = cls(
            name=squadron_dict["name"],
            tag=squadron_dict["tag"],
            minor_faction_names=squadron_dict["minor_faction_names"],
            leaders=squadron_dict["leaders"],
            officers=squadron_dict["officers"],
            members=squadron_dict["members"],
            recruits=squadron_dict["recruits"]
            )
        return squadron


    def get_as_dict(self) -> dict:
        squadron_dict = {}
        squadron_dict["name"] = self.name
        squadron_dict["tag"] = self.tag
        squadron_dict["minor_faction_names"] = self.minor_faction_names
        squadron_dict["leaders"] = self.leaders
        squadron_dict["officers"] = self.officers
        squadron_dict["members"] = self.members
        squadron_dict["recruits"] = self.recruits
        return squadron_dict


    def __str__(self):
        return f"Squadron: {self.name.title()} ({self.tag})"

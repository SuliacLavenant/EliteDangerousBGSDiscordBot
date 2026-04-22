from dataclasses import dataclass, field

@dataclass
class Squadron:
    id: str = None
    minor_faction_names: list = field(default_factory=list)
    name: str = ""
    tag: str = ""

    leader_ids: list = field(default_factory=list)
    officer_ids: list = field(default_factory=list)
    member_ids: list = field(default_factory=list)
    recruit_ids: list = field(default_factory=list)


    @classmethod
    def init_from_dict(cls, squadron_dict: dict):
        squadron = cls(
            id=squadron_dict["id"],
            minor_faction_names=squadron_dict["minor_faction_names"],
            name=squadron_dict["name"],
            tag=squadron_dict["tag"],
            leader_ids=squadron_dict["leader_ids"],
            officer_ids=squadron_dict["officer_ids"],
            member_ids=squadron_dict["member_ids"],
            recruit_ids=squadron_dict["recruit_ids"]
            )
        return squadron


    def get_as_dict(self) -> dict:
        squadron_dict = {}
        squadron_dict["id"] = self.id
        squadron_dict["minor_faction_names"] = self.minor_faction_names
        squadron_dict["name"] = self.name
        squadron_dict["tag"] = self.tag
        squadron_dict["leader_ids"] = self.leader_ids
        squadron_dict["officer_ids"] = self.officer_ids
        squadron_dict["member_ids"] = self.member_ids
        squadron_dict["recruit_ids"] = self.recruit_ids
        return squadron_dict


    def add_minor_faction(self, minor_faction_name: str) -> bool:
        if len(minor_faction_name)==0 and minor_faction_name.lower() in self.minor_faction_names:
            return False
        else:
            self.minor_faction_names.append(minor_faction_name.lower())
            return True


    def remove_minor_faction(self, minor_faction_name: str) -> bool:
        if minor_faction_name.lower() in self.minor_faction_names:
            self.minor_faction_names.remove(minor_faction_name.lower())
            return True
        else:
            return False


    def __str__(self):
        return f"Squadron: {self.name.title()} ({self.tag})"

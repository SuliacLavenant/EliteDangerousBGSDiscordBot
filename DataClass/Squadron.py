from dataclasses import dataclass, field

@dataclass
class Squadron:
    id: int = None
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


    def add_player(self, player_id: int):
        self.recruit_ids.append(player_id)


    def remove_player(self, player_id: int) -> bool:
        if player_id in self.leader_ids:
            self.leader_ids.remove(player_id)
            return True
        elif player_id in self.officer_ids:
            self.officer_ids.remove(player_id)
            return True
        elif player_id in self.member_ids:
            self.member_ids.remove(player_id)
            return True
        elif player_id in self.recruit_ids:
            self.recruit_ids.remove(player_id)
            return True
        else:
            return False


    def get_player_position_in_squadron(self, player_id: int) -> str:
        if player_id in self.leader_ids:
            return "Leader"
        elif player_id in self.officer_ids:
            return "Officer"
        elif player_id in self.member_ids:
            return "Member"
        elif player_id in self.recruit_ids:
            return "Recruit"
        return None


    def get_player_ids(self) -> list:
        return self.leader_ids + self.officer_ids + self.member_ids + self.recruit_ids


    def __str__(self):
        return f"Squadron: {self.name.title()} ({self.tag})"

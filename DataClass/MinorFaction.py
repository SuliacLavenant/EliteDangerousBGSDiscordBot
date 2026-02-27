from dataclasses import dataclass, field

@dataclass
class MinorFaction:
    name: str = ""
    allegiance: str = ""
    government: str = ""

    origin_system_name: str = ""
    system_names: list = field(default_factory=list)


    @classmethod
    def init_from_dict(cls, minor_faction_dict: dict):
        minor_faction = cls(
            name=minor_faction_dict["name"],
            allegiance=minor_faction_dict["allegiance"],
            government=minor_faction_dict["government"],
            origin_system_name=minor_faction_dict["origin_system_name"],
            system_names=minor_faction_dict["system_names"]
            )
        return minor_faction


    def add_system(self, system_name):
        if system_name not in self.system_names:
            self.system_names.append(system_name)
            return True
        else:
            return False


    def remove_system(self, system_name):
        if system_name in self.system_names:
            self.system_names.remove(system_name)
            return True
        else:
            return False


    def get_as_dict(self) -> dict:
        minor_faction_dict = {}
        minor_faction_dict["name"] = self.name
        minor_faction_dict["allegiance"] = self.allegiance
        minor_faction_dict["government"] = self.government
        minor_faction_dict["origin_system_name"] = self.origin_system_name
        minor_faction_dict["system_names"] = self.system_names

        return minor_faction_dict


    def __str__(self):
        return f"Minor Faction: {self.name.title()} | Allegiance: {self.allegiance.title()} | Government: {self.government.title()} | Origin System: {self.origin_system_name.title()} | present in {len(self.system_names)} common systems"

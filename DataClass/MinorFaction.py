from dataclasses import dataclass, field

@dataclass
class MinorFaction:
    name: str = ""
    allegiance: str = ""
    government: str = ""
    origin_system_name: str = ""


    @classmethod
    def init_from_dict(cls, minor_faction_dict: dict):
        minor_faction = cls(
            name=minor_faction_dict["name"],
            allegiance=minor_faction_dict["allegiance"],
            government=minor_faction_dict["government"],
            origin_system_name=minor_faction_dict["origin_system_name"]
            )
        return minor_faction


    def get_as_dict(self) -> dict:
        minor_faction_dict = {}
        minor_faction_dict["name"] = self.name
        minor_faction_dict["allegiance"] = self.allegiance
        minor_faction_dict["government"] = self.government
        minor_faction_dict["origin_system_name"] = self.origin_system_name

        return minor_faction_dict


    def __str__(self):
        return f"Minor Faction: {self.name.title()} | Allegiance: {self.allegiance.title()} | Government: {self.government.title()} | Origin System: {self.origin_system_name.title()}"

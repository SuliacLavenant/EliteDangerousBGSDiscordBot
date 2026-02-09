from dataclasses import dataclass, field

@dataclass
class SystemGroup:
    name: str = ""
    rgb_color: tuple = None
    emote: str = None
    systems: list = field(default_factory=list)

    @classmethod
    def init_from_dict(cls, system_group_dict: dict):
        return cls(
            name = system_group_dict["name"],
            rgb_color = system_group_dict["rgb_color"],
            emote = system_group_dict["emote"],
            systems = system_group_dict["systems"]
        )


    def rename(self, name: str):
        self.name = name


    def set_rgb_color(self, rgb_color: tuple):
        self.rgb_color = rgb_color


    def haveSystem(self, system_name: str):
        return system_name.lower() in self.systems


    def addSystem(self, system_name: str):
        self.systems.append(system_name.lower())


    def add_systems(self, system_name_list: list):
        for system_name in system_name_list:
            self.addSystem(system_name)


    def removeSystem(self, system_name: str):
        if system_name in self.systems:
            self.systems.remove(system_name)
            return True
        else:
            return False


    def remove_systems(self, system_name_list: str):
        removed = True
        for system_name in system_name_list:
            removed = removed and self.removeSystem(system_name)
        return removed


    def get_as_dict(self) -> dict:
        system_group_dict = {}
        system_group_dict["name"] = self.name
        system_group_dict["rgb_color"] = self.rgb_color
        system_group_dict["emote"] = self.emote
        system_group_dict["systems"] = self.systems

        return system_group_dict


    def __str__(self):
        return f"System Group Name: {self.name} | color: {self.rgb_color} | emote: {self.emote} | Systems: {self.systems}"

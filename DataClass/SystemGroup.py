from dataclasses import dataclass, field

@dataclass
class SystemGroup:
    name: str = ""
    color: int = 9936031
    systems: list = field(default_factory=list)

    #init from Dict
    @classmethod
    def initFromDict(cls, systemGroupDict: dict):
        return cls(name=systemGroupDict["name"],color=systemGroupDict["color"],systems=systemGroupDict["systems"])

    def rename(self, name: str):
        self.name = name
    
    def setColor(self, color: int):
        self.color = color
    
    def haveSystem(self, systemName: str):
        return systemName.lower() in self.systems

    def addSystem(self, systemName: str):
        self.systems.append(systemName.lower())

    def removeSystem(self, systemName: str):
        if systemName in self.systems:
            self.systems.remove(systemName)
            return True
        else:
            return False

    def __str__(self):
        return f"System Group Name: {self.name} | color: {self.color} | Systems: {self.systems}"
#custom
from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap
from DataClass.SystemGroup import SystemGroup

class SystemsRecapViews:
    def getRawSystemsMinorFactionRecapEmbeds(systemsRecap: dict):
        systemNames = list(systemsRecap.keys())
        systemNames.sort()

        titleSet = False
        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = systemsRecap[systemName]
            if len(systems)>=20:
                if not titleSet:
                    embeds.append(SystemsRecapView(systems, "Raw Systems Recap").getEmbed())
                    titleSet = True
                else:
                    embeds.append(SystemsRecapView(systems).getEmbed())
                systems = {}
        if len(systems)>0:
            embeds.append(SystemsRecapView(systems).getEmbed())

        return embeds
    
    def getSystemsMinorFactionRecapEmbeds(systemRecaps: dict, systemGroups: list, systemsWithNoGroups: list):
        embeds=[]
        for systemGroup in systemGroups:
            systemNames = systemGroup.systems
            if systemNames!=None and len(systemNames)>0:
                systemNames.sort()
                embeds += SystemsRecapViews.getSystemGroupRecapEmbeds(systemRecaps,systemNames,systemGroup.name)

        if len(systemsWithNoGroups)>0:
            systemsWithNoGroups.sort()
            embeds += SystemsRecapViews.getSystemGroupRecapEmbeds(systemRecaps,systemsWithNoGroups)
        return embeds

    def getSystemGroupRecapEmbeds(systemRecaps: dict, systemNames: list, groupName: str = "Other"):
        titleSet = False
        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = systemRecaps[systemName]
            if len(systems)>=20:
                if not titleSet:
                    embeds.append(SystemsRecapView(systems, groupName).getEmbed())
                    titleSet = True
                else:
                    embeds.append(SystemsRecapView(systems).getEmbed())
                systems = {}
        if len(systems)>0:
            embeds.append(SystemsRecapView(systems).getEmbed())

        return embeds

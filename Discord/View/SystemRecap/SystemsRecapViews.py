#custom
from Discord.View.SystemRecap.SystemsRecapView import SystemsRecapView
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

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
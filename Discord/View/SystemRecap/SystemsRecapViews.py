import discord

#custom
from Discord.View.SystemRecap.GeneralSystemsRecapView import GeneralSystemsRecapView
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
            if len(systems)>=15:
                if not titleSet:
                    embeds.append(GeneralSystemsRecapView(systems, "Raw Systems Recap").getEmbed())
                    titleSet = True
                else:
                    embeds.append(GeneralSystemsRecapView(systems).getEmbed())
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(systems).getEmbed())

        return embeds
    
    def getSystemsMinorFactionRecapEmbeds(systemRecaps: dict, systemGroups: list, systemsWithNoGroups: list):
        embeds=[]
        for systemGroup in systemGroups:
            systemNames = systemGroup.systems
            if systemNames!=None and len(systemNames)>0:
                systemNames.sort()
                embeds += SystemsRecapViews.getSystemGroupRecapEmbeds(systemRecaps,systemNames,systemGroup.name,discord.Color(systemGroup.color))

        if len(systemsWithNoGroups)>0:
            systemsWithNoGroups.sort()
            embeds += SystemsRecapViews.getSystemGroupRecapEmbeds(systemRecaps,systemsWithNoGroups)
        return embeds

    def getSystemGroupRecapEmbeds(systemRecaps: dict, systemNames: list, groupName: str = "Other", color: discord.Color = None):
        titleSet = False
        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = systemRecaps[systemName]
            if len(systems)>=20:
                if not titleSet:
                    embeds.append(GeneralSystemsRecapView(systems, color, groupName).getEmbed())
                    titleSet = True
                else:
                    embeds.append(GeneralSystemsRecapView(systems, color).getEmbed())
                systems = {}
        if len(systems)>0:
            if not titleSet:
                embeds.append(GeneralSystemsRecapView(systems, color, groupName).getEmbed())
            else:
                embeds.append(GeneralSystemsRecapView(systems, color).getEmbed())

        return embeds

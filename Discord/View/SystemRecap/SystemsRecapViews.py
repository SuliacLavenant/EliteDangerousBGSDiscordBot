import discord

#custom
from Discord.View.SystemRecap.GeneralSystemsRecapView import GeneralSystemsRecapView
from Discord.View.SystemRecap.Warning.ExpansionWarningSystemsRecapView import ExpansionWarningSystemsRecapView
from Discord.View.SystemRecap.Warning.InfluenceMarginWarningSystemsRecapView import InfluenceMarginWarningSystemsRecapView
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap
from DataClass.SystemGroup import SystemGroup

class SystemsRecapViews:
    def __init__(self, systemRecapsDict: dict, systemGroups: list, systemsWithNoGroups: list):
        self.systemRecapsDict = systemRecapsDict
        self.systemGroups = systemGroups
        self.systemsWithNoGroups = systemsWithNoGroups

        for systemGroup in self.systemGroups:
            for systemName in systemGroup.systems:
                self.systemRecapsDict[systemName].systemGroup = systemGroup


    def getRawSystemsMinorFactionRecapEmbeds(self):
        systemNames = list(self.systemRecapsDict.keys())
        systemNames.sort()

        titleSet = False
        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = self.systemRecapsDict[systemName]
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
    
    def getSystemsMinorFactionRecapEmbeds(self):
        embeds=[]
        for systemGroup in self.systemGroups:
            systemNames = systemGroup.systems
            if systemNames!=None and len(systemNames)>0:
                systemNames.sort()
                embeds += self.getSystemGroupRecapEmbeds(systemNames,systemGroup)

        if len(self.systemsWithNoGroups)>0:
            self.systemsWithNoGroups.sort()
            embeds += self.getSystemGroupRecapEmbeds(self.systemsWithNoGroups, None)
        return embeds

    def getSystemGroupRecapEmbeds(self, systemNames: list, systemGroup: SystemGroup):
        title = None
        color = None
        if systemGroup!=None:
            title = systemGroup.name
            color = discord.Color(systemGroup.color)
            if systemGroup.emote != None:
                title = f"{systemGroup.emote} {title} {systemGroup.emote}"
        else:
            title = "Other"

        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = self.systemRecapsDict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())

        return embeds

    def getExpansionWarningSystemRecapEmbeds(self):
        systemRecapsInExpansionWarning = {}
        for systemRecapName in self.systemRecapsDict:
            if self.systemRecapsDict[systemRecapName].expansionWarning:
                systemRecapsInExpansionWarning[str(self.systemRecapsDict[systemRecapName].influence)] = self.systemRecapsDict[systemRecapName]

        embeds = []
        titleSet = False
        systems = {}
        for systemRecap in systemRecapsInExpansionWarning.values():
            systems[systemRecap.system.name] = systemRecap
            if len(systems)>=15:
                embeds.append(ExpansionWarningSystemsRecapView(systems, not titleSet).getEmbed())
                titleSet = True
                systems = {}
        if len(systems)>0:
            if not titleSet:
                embeds.append(ExpansionWarningSystemsRecapView(systems, not titleSet).getEmbed())

        return embeds
    
    def getInfluenceMarginWarningSystemRecapEmbeds(self):
        warningLvl = {}
        warningLvl[3] = []
        warningLvl[2] = []
        warningLvl[1] = []
        for systemRecapName in self.systemRecapsDict:
            systemRecap = self.systemRecapsDict[systemRecapName]
            if systemRecap.marginWarning:
                match systemRecap.influenceWarningLevel:
                    case 3:
                        warningLvl[3].append(systemRecapName)
                    case 2:
                        warningLvl[2].append(systemRecapName)
                    case 1:
                        warningLvl[1].append(systemRecapName)

        embeds = {}
        embeds[3] = []
        embeds[2] = []
        embeds[1] = []
        
        for lvl in warningLvl.keys():
            titleSet = False
            systems = {}
            for systemRecapName in warningLvl[lvl]:
                systems[systemRecapName] = self.systemRecapsDict[systemRecapName]
                if len(systems)>=15:
                    embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(systems, lvl, not titleSet).getEmbed())
                    titleSet = True
                    systems = {}
            if len(systems)>0:
                if not titleSet:
                    embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(systems, lvl, not titleSet).getEmbed())

        return embeds

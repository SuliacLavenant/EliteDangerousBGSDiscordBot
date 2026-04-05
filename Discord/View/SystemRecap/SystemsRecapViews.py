import discord

#custom
from BotConfig.BotConfig import BotConfig
from Discord.View.SystemRecap.GeneralSystemsRecapView import GeneralSystemsRecapView
from Discord.View.SystemRecap.Warning.ConflictSystemsRecapView import ConflictSystemsRecapView
from Discord.View.SystemRecap.Warning.ExpansionWarningSystemsRecapView import ExpansionWarningSystemsRecapView
from Discord.View.SystemRecap.Warning.InfluenceMarginWarningSystemsRecapView import InfluenceMarginWarningSystemsRecapView
from Discord.View.SystemRecap.Warning.RetreatWarningSystemsRecapView import RetreatWarningSystemsRecapView
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


    ############## systems recap
    def getSystemsMinorFactionRecapEmbeds(self):
        embeds=[]
        for systemGroup in self.systemGroups:
            if systemGroup.systems!=None and len(systemGroup.systems)>0:
                systemGroup.calculate_number_leader_systems(self.systemRecapsDict)
                systemGroup.systems.sort()
                embeds += self.getSystemGroupRecapEmbeds(systemGroup)

        if len(self.systemsWithNoGroups)>0:
            embeds += self.getSystemNoGroupRecapEmbeds()
        return embeds

    def getSystemGroupRecapEmbeds(self, systemGroup: SystemGroup):
        title = systemGroup.name
        color = None
        if systemGroup.rgb_color != None:
            color = discord.Color.from_rgb(systemGroup.rgb_color[0],systemGroup.rgb_color[1],systemGroup.rgb_color[2])
        if systemGroup.emote != None:
            title = f"{systemGroup.emote} {systemGroup.name} {systemGroup.emote}"
        title += f" ({systemGroup.number_leader_systems} {BotConfig.emotes.minorFaction.positionInSystem.leader} | {len(systemGroup.systems)} {BotConfig.emotes.systems})"

        embeds=[]
        systems = {}
        for systemName in systemGroup.systems:
            systems[systemName] = self.systemRecapsDict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())

        return embeds


    def getSystemNoGroupRecapEmbeds(self):
        self.systemsWithNoGroups.sort()
        number_leader_systems = 0
        for system_name in self.systemsWithNoGroups:
            if self.systemRecapsDict[system_name].isLeader:
                number_leader_systems += 1

        title = f"Other ({number_leader_systems} {BotConfig.emotes.minorFaction.positionInSystem.leader} | {len(self.systemsWithNoGroups)} {BotConfig.emotes.systems})"
        color = None

        embeds=[]
        systems = {}
        for systemName in self.systemsWithNoGroups:
            systems[systemName] = self.systemRecapsDict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(systems, color, title).getEmbed())

        return embeds
    ##############


    ############## Conflict
    def getConflictSystemRecapEmbeds(self):
        systemNamesInConflict = []
        for systemName in self.systemRecapsDict:
            if self.systemRecapsDict[systemName].inConflict:
                systemNamesInConflict.append(systemName)

        embeds = []
        titleSet = False
        systems = {}
        for systemName in systemNamesInConflict:
            systems[systemName] = self.systemRecapsDict[systemName]
            if len(systems)>=15:
                embeds.append(ConflictSystemsRecapView(systems, not titleSet).getEmbed())
                titleSet = True
                systems = {}
        if len(systems)>0:
            if not titleSet:
                embeds.append(ConflictSystemsRecapView(systems, not titleSet).getEmbed())

        return embeds


    ############## Expansion Warning
    def getExpansionWarningSystemRecapEmbeds(self):
        systemNamesInExpansionWarning = []
        for systemName in self.systemRecapsDict:
            if self.systemRecapsDict[systemName].expansionWarning:
                systemNamesInExpansionWarning.append(systemName)
        systemNamesInExpansionWarning = self.sortListByInfluence(systemNamesInExpansionWarning)

        embeds = []
        titleSet = False
        systems = {}
        for systemName in systemNamesInExpansionWarning:
            systems[systemName] = self.systemRecapsDict[systemName]
            if len(systems)>=15:
                embeds.append(ExpansionWarningSystemsRecapView(systems, not titleSet).getEmbed())
                titleSet = True
                systems = {}
        if len(systems)>0:
            if not titleSet:
                embeds.append(ExpansionWarningSystemsRecapView(systems, not titleSet).getEmbed())

        return embeds


    ############## Retreat Warning
    def get_retreat_warning_system_recap_embeds(self):
        system_names_in_retreat_warning = []
        for system_name in self.systemRecapsDict:
            if self.systemRecapsDict[system_name].retreatWarning:
                system_names_in_retreat_warning.append(system_name)
        system_names_in_retreat_warning = self.sortListByInfluence(system_names_in_retreat_warning)

        embeds = []
        title_set = False
        systems = {}
        for system_name in system_names_in_retreat_warning:
            systems[system_name] = self.systemRecapsDict[system_name]
            if len(systems)>=15:
                embeds.append(RetreatWarningSystemsRecapView(systems, not title_set).getEmbed())
                title_set = True
                systems = {}
        if len(systems)>0:
            if not title_set:
                embeds.append(RetreatWarningSystemsRecapView(systems, not title_set).getEmbed())

        return embeds
    

    ############## Influence Margin Warning
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
        
        warningLvl[3] = self.sortListByInfluenceMargin(warningLvl[3])
        warningLvl[2] = self.sortListByInfluenceMargin(warningLvl[2])
        warningLvl[1] = self.sortListByInfluenceMargin(warningLvl[1])

        embeds = {}
        embeds[1] = []
        embeds[2] = []
        embeds[3] = []
        
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


    ############## SORT ALGOS ##############

    def sortListByInfluence(self, systemNameList: list) -> list:
        for i in range(1,len(systemNameList)):
            tmp = systemNameList[i]
            j = i-1
            while j>=0 and self.systemRecapsDict[systemNameList[j]].influence < self.systemRecapsDict[tmp].influence:
                systemNameList[j+1] = systemNameList[j]
                j-=1
            systemNameList[j+1] = tmp
        
        return systemNameList


    def sortListByInfluenceMargin(self, systemNameList: list) -> list:
        for i in range(1,len(systemNameList)):
            tmp = systemNameList[i]
            j = i-1
            while j>=0 and self.systemRecapsDict[systemNameList[j]].leaderInfluenceMargin < self.systemRecapsDict[tmp].leaderInfluenceMargin:
                systemNameList[j+1] = systemNameList[j]
                j-=1
            systemNameList[j+1] = tmp
        
        return systemNameList

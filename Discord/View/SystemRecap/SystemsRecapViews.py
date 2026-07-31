import discord

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.GuildSettings import GuildSettings
from Discord.View.SystemRecap.GeneralSystemsRecapView import GeneralSystemsRecapView
from Discord.View.SystemRecap.Warning.ConflictSystemsRecapView import ConflictSystemsRecapView
from Discord.View.SystemRecap.Warning.ExpansionWarningSystemsRecapView import ExpansionWarningSystemsRecapView
from Discord.View.SystemRecap.Warning.InfluenceMarginWarningSystemsRecapView import InfluenceMarginWarningSystemsRecapView
from Discord.View.SystemRecap.Warning.RetreatWarningSystemsRecapView import RetreatWarningSystemsRecapView
from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap
from DataClass.SystemGroup import SystemGroup

class SystemsRecapViews:
    guild_settings: GuildSettings
    system_recap_dict: dict[str,SystemMinorFactionRecap]

    def __init__(self, guild_settings: GuildSettings, system_recap_dict: dict[str,SystemMinorFactionRecap], systemGroups: list, systemsWithNoGroups: list):
        self.guild_settings = guild_settings
        self.system_recap_dict = system_recap_dict
        self.systemGroups = systemGroups
        self.systemsWithNoGroups = systemsWithNoGroups

        for systemGroup in self.systemGroups:
            for systemName in systemGroup.systems:
                self.system_recap_dict[systemName].systemGroup = systemGroup


    def getRawSystemsMinorFactionRecapEmbeds(self):
        systemNames = list(self.system_recap_dict.keys())
        systemNames.sort()

        titleSet = False
        embeds=[]
        systems = {}
        for systemName in systemNames:
            systems[systemName] = self.system_recap_dict[systemName]
            if len(systems)>=15:
                if not titleSet:
                    embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, "Raw Systems Recap").getEmbed())
                    titleSet = True
                else:
                    embeds.append(GeneralSystemsRecapView(self.guild_settings, systems).getEmbed())
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(self.guild_settings, systems).getEmbed())

        return embeds


    ############## systems recap
    def getSystemsMinorFactionRecapEmbeds(self):
        embeds=[]
        for systemGroup in self.systemGroups:
            if systemGroup.systems!=None and len(systemGroup.systems)>0:
                systemGroup.calculate_number_leader_systems(self.system_recap_dict)
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
            systems[systemName] = self.system_recap_dict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).getEmbed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).getEmbed())

        return embeds


    def getSystemNoGroupRecapEmbeds(self):
        self.systemsWithNoGroups.sort()
        number_leader_systems = 0
        for system_name in self.systemsWithNoGroups:
            if self.system_recap_dict[system_name].isLeader:
                number_leader_systems += 1

        title = f"Other ({number_leader_systems} {BotConfig.emotes.minorFaction.positionInSystem.leader} | {len(self.systemsWithNoGroups)} {BotConfig.emotes.systems})"
        color = None

        embeds=[]
        systems = {}
        for systemName in self.systemsWithNoGroups:
            systems[systemName] = self.system_recap_dict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).getEmbed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).getEmbed())

        return embeds
    ##############


##################################################
################################################## Conflict Recap

    def get_conflict_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_conflict: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].inConflict:
                system_names_in_conflict.append(system_name)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_conflict:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(ConflictSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(ConflictSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())

        return embeds


##################################################
################################################## Warning Recap

    def get_expansion_warning_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_expansion_warning: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].expansionWarning:
                system_names_in_expansion_warning.append(system_name)
        system_names_in_expansion_warning = self.sort_list_by_influence(system_names_in_expansion_warning)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_expansion_warning:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(ExpansionWarningSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(ExpansionWarningSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())

        return embeds


    def get_retreat_warning_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_retreat_warning: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].retreatWarning:
                system_names_in_retreat_warning.append(system_name)
        system_names_in_retreat_warning = self.sort_list_by_influence(system_names_in_retreat_warning)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_retreat_warning:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(RetreatWarningSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(RetreatWarningSystemsRecapView(self.guild_settings, systems, not title_set).getEmbed())

        return embeds
    

    def get_influence_margin_warning_system_recap_embeds(self) -> dict[int,list]:
        warning_lvl: dict[int,list] = {}
        warning_lvl[3]: list[str] = []
        warning_lvl[2]: list[str] = []
        warning_lvl[1]: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].marginWarning:
                match self.system_recap_dict[system_name].influenceWarningLevel:
                    case 3:
                        if not self.system_recap_dict[system_name].inConflict:
                            warning_lvl[3].append(system_name)
                    case 2:
                        warning_lvl[2].append(system_name)
                    case 1:
                        warning_lvl[1].append(system_name)
        
        warning_lvl[3] = self.sort_list_by_influence_margin(warning_lvl[3])
        warning_lvl[2] = self.sort_list_by_influence_margin(warning_lvl[2])
        warning_lvl[1] = self.sort_list_by_influence_margin(warning_lvl[1])

        embeds: dict[str,list] = {}
        embeds[1]: list[discord.Embed] = []
        embeds[2]: list[discord.Embed] = []
        embeds[3]: list[discord.Embed] = []
        
        for lvl in warning_lvl.keys():
            title_set: bool = False
            systems: dict[str,SystemMinorFactionRecap] = {}
            for system_name in warning_lvl[lvl]:
                systems[system_name] = self.system_recap_dict[system_name]
                if len(systems)>=15:
                    embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(self.guild_settings, systems, lvl, not title_set).getEmbed())
                    title_set = True
                    systems = {}
            if len(systems)>0:
                embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(self.guild_settings, systems, lvl, not title_set).getEmbed())

        return embeds


##################################################
################################################## SORT ALGOS

    def sort_list_by_influence(self, system_names: list[str]) -> list[str]:
        for i in range(1,len(system_names)):
            tmp = system_names[i]
            j = i-1
            while j>=0 and self.system_recap_dict[system_names[j]].influence < self.system_recap_dict[tmp].influence:
                system_names[j+1] = system_names[j]
                j-=1
            system_names[j+1] = tmp
        
        return system_names


    def sort_list_by_influence_margin(self, system_names: list[str]) -> list[str]:
        for i in range(1,len(system_names)):
            tmp = system_names[i]
            j = i-1
            while j>=0 and self.system_recap_dict[system_names[j]].leaderInfluenceMargin < self.system_recap_dict[tmp].leaderInfluenceMargin:
                system_names[j+1] = system_names[j]
                j-=1
            system_names[j+1] = tmp
        
        return system_names

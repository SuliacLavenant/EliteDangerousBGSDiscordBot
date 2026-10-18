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

    def __init__(self, guild_settings: GuildSettings, system_recap_dict: dict[str,SystemMinorFactionRecap], system_groups: list, system_names_with_no_group: list):
        self.guild_settings = guild_settings
        self.system_recap_dict = system_recap_dict
        self.system_groups = system_groups
        self.system_names_with_no_group = system_names_with_no_group

        system_names_to_remove: list[str] = []

        # TODO I think I can remove this
        # for system_group in self.system_groups:
        #     for system_name in system_group.systems:
        #         if system_name in system_recap_dict.keys():
        #             self.system_recap_dict[system_name].systemGroup = system_group
        #         else:
        #             system_names_to_remove.append(system_name)
        #     for system_name in system_names_to_remove:
        #         system_group.systems.remove(system_name)
        #     system_names_to_remove = []

        # for system_name in self.system_names_with_no_group:
        #     if system_name not in system_recap_dict.keys():
        #         system_names_to_remove.append(system_name)
        # for system_name in system_names_to_remove:
        #     self.system_names_with_no_group.remove(system_name)
        # system_names_to_remove = []


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
    def get_systems_minor_faction_recap_embeds(self):
        embeds=[]
        for system_group in self.system_groups:
            if system_group.systems is not None and len(system_group.systems)>0:
                system_group.calculate_number_leader_systems(self.system_recap_dict)
                # system_group.systems.sort()
                embeds += self.get_system_group_recap_embeds(system_group)

        if len(self.system_names_with_no_group)>0:
            embeds += self.get_system_no_group_recap_embeds()
        return embeds


    def get_system_group_recap_embeds(self, system_group: SystemGroup):
        title: str = system_group.name
        color = None
        if system_group.color_rgb != None:
            color = discord.Color.from_rgb(system_group.color_rgb[0], system_group.color_rgb[1], system_group.color_rgb[2])
        if system_group.emote != None:
            title = f"{system_group.emote} {system_group.name} {system_group.emote}"
        title += f" ({system_group.number_leader_systems} {BotConfig.emotes.minorFaction.positionInSystem.leader} | {len(system_group.systems)} {BotConfig.emotes.systems})"

        embeds=[]
        system_recaps = {}
        for tracked_system in system_group.systems:
            system_recaps[tracked_system.system.name] = self.system_recap_dict[tracked_system.system.name]
            if len(system_recaps) >= 15:
                embeds.append(GeneralSystemsRecapView(self.guild_settings, system_recaps, color, title).get_embed())
                title = None
                system_recaps = {}
        if len(system_recaps)>0:
            embeds.append(GeneralSystemsRecapView(self.guild_settings, system_recaps, color, title).get_embed())

        return embeds


    def get_system_no_group_recap_embeds(self):
        self.system_names_with_no_group.sort()
        number_leader_systems = 0
        for system_name in self.system_names_with_no_group:
            if self.system_recap_dict[system_name].is_leader:
                number_leader_systems += 1

        title = f"Other ({number_leader_systems} {BotConfig.emotes.minorFaction.positionInSystem.leader} | {len(self.system_names_with_no_group)} {BotConfig.emotes.systems})"
        color = None

        embeds=[]
        systems = {}
        for systemName in self.system_names_with_no_group:
            systems[systemName] = self.system_recap_dict[systemName]
            if len(systems)>=15:
                embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).get_embed())
                title = None
                systems = {}
        if len(systems)>0:
            embeds.append(GeneralSystemsRecapView(self.guild_settings, systems, color, title).get_embed())

        return embeds
    ##############


##################################################
################################################## Conflict Recap

    def get_conflict_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_conflict: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].in_conflict:
                system_names_in_conflict.append(system_name)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_conflict:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(ConflictSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(ConflictSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())

        return embeds


##################################################
################################################## Warning Recap

    def get_expansion_warning_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_expansion_warning: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].expansion_warning:
                system_names_in_expansion_warning.append(system_name)
        system_names_in_expansion_warning = self.sort_list_by_influence(system_names_in_expansion_warning)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_expansion_warning:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(ExpansionWarningSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(ExpansionWarningSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())

        return embeds


    def get_retreat_warning_system_recap_embeds(self) -> list[discord.Embed]:
        system_names_in_retreat_warning: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].expansion_warning:
                system_names_in_retreat_warning.append(system_name)
        system_names_in_retreat_warning = self.sort_list_by_influence(system_names_in_retreat_warning)

        embeds: list[discord.Embed] = []
        title_set: bool = False
        systems: dict[str,SystemMinorFactionRecap] = {}
        for system_name in system_names_in_retreat_warning:
            systems[system_name] = self.system_recap_dict[system_name]
            if len(systems)>=15:
                embeds.append(RetreatWarningSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())
                title_set = True
                systems = {}
        if len(systems)>0:
            embeds.append(RetreatWarningSystemsRecapView(self.guild_settings, systems, not title_set).get_embed())

        return embeds
    

    def get_influence_margin_warning_system_recap_embeds(self) -> dict[int,list]:
        warning_lvl: dict[int,list] = {}
        warning_lvl[3]: list[str] = []
        warning_lvl[2]: list[str] = []
        warning_lvl[1]: list[str] = []
        for system_name in self.system_recap_dict:
            if self.system_recap_dict[system_name].margin_warning:
                match self.system_recap_dict[system_name].influence_warning_level:
                    case 3:
                        if not self.system_recap_dict[system_name].in_conflict:
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
                    embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(self.guild_settings, systems, lvl, not title_set).get_embed())
                    title_set = True
                    systems = {}
            if len(systems)>0:
                embeds[lvl].append(InfluenceMarginWarningSystemsRecapView(self.guild_settings, systems, lvl, not title_set).get_embed())

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
            while j>=0 and self.system_recap_dict[system_names[j]].leader_influence_margin < self.system_recap_dict[tmp].leader_influence_margin:
                system_names[j+1] = system_names[j]
                j-=1
            system_names[j+1] = tmp
        
        return system_names

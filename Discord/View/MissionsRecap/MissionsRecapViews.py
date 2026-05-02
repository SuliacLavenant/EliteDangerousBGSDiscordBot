import discord

from DataClass.Mission.SystemMission.RetreatMinorFactionFromSystemMission import RetreatMinorFactionFromSystemMission
from DataClass.Mission.SystemMission.SetMinorFactionAsLeaderInSystemMission import SetMinorFactionAsLeaderInSystemMission
from DataStorageManager import DataStorageManager
from Discord.View.MissionsRecap.RetreatMinorFactionFromSystemMissionsRecapView import RetreatMinorFactionFromSystemMissionsRecapView
from Discord.View.MissionsRecap.SetMinorFactionAsLeaderInSystemMissionsRecapView import SetMinorFactionAsLeaderInSystemMissionsRecapView
from Discord.View.MissionsRecap.SystemMissionsRecapPerSystemView import SystemMissionsRecapPerSystemView

class MissionsRecapViews:
    guild_id: int = None
    retreat_missions: list = None
    set_leader_mission: list = None

    missions_per_system: dict = None


    def __init__(self, guild_id):
        self.guild_id = guild_id
        missions = DataStorageManager.get_missions(self.guild_id)

        self.missions_per_system = {}
        self.retreat_missions = []
        self.set_leader_mission = []
        for mission in missions:
            match mission.mission_type:
                case "RetreatMinorFactionFromSystemMission":
                    self.retreat_missions.append(mission)
                    if mission.system_name not in self.missions_per_system.keys():
                        self.missions_per_system[mission.system_name] = []
                    self.missions_per_system[mission.system_name].append(mission)
                case "SetMinorFactionAsLeaderInSystemMission":
                    self.set_leader_mission.append(mission)
                    if mission.system_name not in self.missions_per_system.keys():
                        self.missions_per_system[mission.system_name] = []
                    self.missions_per_system[mission.system_name].append(mission)

        self.process_retreat_mission()
        self.process_set_leader_mission()


    def process_retreat_mission(self):
        for mission in self.retreat_missions:
            mission.update_with_system_data(DataStorageManager.get_system(self.guild_id,mission.system_name))
            mission.check_mission_state()


    def process_set_leader_mission(self):
        for mission in self.set_leader_mission:
            mission.update_with_system_data(DataStorageManager.get_system(self.guild_id,mission.system_name))
            mission.check_mission_state()


    def get_retreat_minor_faction_from_system_missions_recap_embeds(self):
        embeds = []
        titleSet = False
        missions = []
        for mission in self.retreat_missions:
            missions.append(mission)
            if len(missions)>=15:
                embeds.append(RetreatMinorFactionFromSystemMissionsRecapView(missions, not titleSet).getEmbed())
                titleSet = True
                missions = []
        if len(missions)>0:
            if not titleSet:
                embeds.append(RetreatMinorFactionFromSystemMissionsRecapView(missions, not titleSet).getEmbed())

        return embeds


    def get_set_minor_faction_as_leader_in_system_missions_recap_embeds(self):
        embeds = []
        titleSet = False
        missions = []
        for mission in self.set_leader_mission:
            missions.append(mission)
            if len(missions)>=15:
                embeds.append(SetMinorFactionAsLeaderInSystemMissionsRecapView(missions, not titleSet).getEmbed())
                titleSet = True
                missions = []
        if len(missions)>0:
            if not titleSet:
                embeds.append(SetMinorFactionAsLeaderInSystemMissionsRecapView(missions, not titleSet).getEmbed())

        return embeds


    def get_missions_recap_per_system_views(self):
        views = []
        for system_missions in self.missions_per_system.values():
            views.append(SystemMissionsRecapPerSystemView(system_missions[0].system, system_missions))

        return views
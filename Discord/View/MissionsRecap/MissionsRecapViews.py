import discord

from DataClass.Mission.SystemMission.RetreatMinorFactionFromSystemMission import RetreatMinorFactionFromSystemMission
from DataStorageManager import DataStorageManager
from Discord.View.MissionsRecap.RetreatMinorFactionFromSystemMissionsRecapView import RetreatMinorFactionFromSystemMissionsRecapView

class MissionsRecapViews:
    guild_id: int = None
    retreat_missions: list = None


    def __init__(self, guild_id):
        self.guild_id = guild_id
        missions = DataStorageManager.get_missions(self.guild_id)

        self.retreat_missions = []
        for mission in missions:
            match mission.mission_type:
                case "RetreatMinorFactionFromSystemMission":
                    self.retreat_missions.append(mission)
        
        self.process_retreat_mission()


    def process_retreat_mission(self):
        for mission in self.retreat_missions:
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

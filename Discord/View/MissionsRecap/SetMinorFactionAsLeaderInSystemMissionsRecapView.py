from datetime import datetime, timezone
import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.Mission.SystemMission.SetMinorFactionAsLeaderInSystemMission import SetMinorFactionAsLeaderInSystemMission
from DataClass.System import System
from Discord.View.MissionsRecap.SystemMissionsRecapView import SystemMissionsRecapView

class SetMinorFactionAsLeaderInSystemMissionsRecapView(SystemMissionsRecapView):
    mission_list: list


    def __init__(self, mission_list: list, is_title: bool = False):
        super().__init__(mission_list,is_title)
        self.color = discord.Color.green()
        if is_title:
            self.title = f"Set Minor Faction As Leader In System"


    def get_mission_recap_one_line(self, mission: SetMinorFactionAsLeaderInSystemMission):
        systemLine = f"{self.get_mission_state_emote(mission)} | **{mission.minor_faction_name}** | {mission.system.name} | {self.get_target_minor_faction_influence_difference_string(mission)} {self.get_last_update_warning(mission.system)}"
        return systemLine

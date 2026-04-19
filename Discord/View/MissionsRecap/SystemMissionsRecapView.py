from datetime import datetime, timezone
import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.Mission.MissionProgressEnum import MissionProgressEnum
from DataClass.Mission.SystemMission.SystemMission import SystemMission
from DataClass.System import System

class SystemMissionsRecapView(discord.ui.View):
    color: discord.Color = ""
    mission_list: list
    title: str = ""


    def __init__(self, mission_list: list, is_title: bool = False):
        super().__init__()
        self.mission_list = mission_list
        self.is_title = is_title


    def getEmbed(self):
        description=""
        for mission in self.mission_list:
            description += self.get_mission_recap_one_line(mission)
            description += "\n"
        if self.color!=None:
            embed = discord.Embed(title=self.title, description=description, color=self.color)
        else:
            embed = discord.Embed(title=self.title, description=description)
        return embed


    def get_last_update_warning(self, system: System):
        time_since_last_update = datetime.now(timezone.utc) - datetime.fromtimestamp(system.lastInfluenceUpdate, tz=timezone.utc)
        days_since_last_update = time_since_last_update.days
        if days_since_last_update<=1:
            return ""
        else:
            return f" | ({BotConfig.emotes.warning}{days_since_last_update} days)"


    def get_mission_recap_one_line(self, mission: SystemMission):
        systemLine = f"{self.get_mission_state_emote(mission)} | {mission.system}"
        return systemLine


    def get_system_name_with_inara_link(self, system: System):
        return f"[**{system.name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(system.name)})"

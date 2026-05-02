from datetime import datetime, timezone
import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig
from DataClass.Mission.SystemMission.SystemMission import SystemMission
from DataClass.System import System

class SystemMissionsRecapPerSystemView(discord.ui.View):
    color: discord.Color = None
    mission_list: list
    system: System


    def __init__(self, system: System, mission_list: list):
        super().__init__()
        self.mission_list = mission_list
        self.system = system

        self.add_item(discord.ui.Button(
            label="Inara",
            url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system.name)}",
            emoji="🌐",
            row=0
        ))


    def get_embed(self):
        title = f"{self.system.name} {self.get_last_update_warning(self.mission_list[0].system)}"
        if self.color!=None:
            embed = discord.Embed(title=title, description="", color=self.color)
        else:
            embed = discord.Embed(title=title, description="")

        for mission in self.mission_list:
            match mission.mission_type:
                case "SetMinorFactionAsLeaderInSystemMission":
                    mission_title = f"{BotConfig.indent2}{BotConfig.emotes.minorFaction.positionInSystem.leader} Set Leader {BotConfig.emotes.minorFaction.positionInSystem.leader} | {mission.get_mission_state_emote()}"
                    mission_description = ""
                    mission_description += f"{BotConfig.indent4} Target: **{mission.minor_faction_name.title()}**\n"
                    mission_description += f"{BotConfig.indent4} Influence Diff: {mission.get_target_minor_faction_influence_difference_string()}"
                    embed.add_field(name=mission_title, value=mission_description, inline=False)
                case "RetreatMinorFactionFromSystemMission":
                    mission_title = f"{BotConfig.indent2}{BotConfig.emotes.minorFaction.state.retreat} Retreat Minor Faction {BotConfig.emotes.minorFaction.state.retreat} | {mission.get_mission_state_emote()}"
                    mission_description = ""
                    mission_description += f"{BotConfig.indent4} Target: **{mission.minor_faction_name.title()}**\n"
                    mission_description += f"{BotConfig.indent4} Current Influence: {mission.get_current_influence_string()}\n"
                    embed.add_field(name=mission_title, value=mission_description, inline=False)

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


    def get_system_name_with_inara_link(self):
        return f"[**{self.system.name}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system.name)})"

import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig

class MissionRecapLegendView(discord.ui.View):


    def __init__(self):
        super().__init__()
        self.title = "Mission Legend"


    def get_embed(self):
        description=""
        embed = discord.Embed(title=self.title, description=description, color=discord.Color.from_rgb(255,255,255))

        ##### Mission Type
        mission_type = f"{BotConfig.emotes.minorFaction.positionInSystem.leader} Set Leader {BotConfig.emotes.minorFaction.positionInSystem.leader}: Bring the influence of the target minor faction over the system leader's influence.\n"
        mission_type += f"{BotConfig.emotes.minorFaction.state.retreat} Retreat Minor Faction {BotConfig.emotes.minorFaction.state.retreat}: Lower the minor faction's influence to below {round(BotConfig.bgs.state.retreat.trigger_influence*100,1)}%.\n"
        embed.add_field(name=f"Mission Type", value=mission_type, inline=False)

        ##### Mission State
        mission_state = f"{BotConfig.emotes.mission.state.upcoming}: The mission has not started yet..\n"
        mission_state += f"{BotConfig.emotes.mission.state.active}: The mission is active and needs to be completed.\n"
        mission_state += f"{BotConfig.emotes.mission.state.pending}: The mission is not yet complete, but it does not require pilot intervention.\n"
        mission_state += f"{BotConfig.emotes.mission.state.complete}: The mission is complete.\n"
        embed.add_field(name=f"Mission State", value=mission_state, inline=False)

        return embed

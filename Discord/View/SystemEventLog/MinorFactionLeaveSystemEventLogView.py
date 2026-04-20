import discord

from BotConfig.BotConfig import BotConfig
from Discord.View.SystemEventLog.SystemEventLogView import SystemEventLogView
from EventClass.SystemEvent.MinorFactionLeaveSystemEvent import MinorFactionLeaveSystemEvent

class MinorFactionLeaveSystemEventLogView(SystemEventLogView):
    system_event: MinorFactionLeaveSystemEvent

    def __init__(self, system_event: MinorFactionLeaveSystemEvent):
        super().__init__(system_event)


    def get_embed(self):
        emote = f"{BotConfig.emotes.arrow.right}{BotConfig.emotes.minorFaction.state.retreat}"
        title = f"{emote}{BotConfig.indent}Minor Faction leave System{BotConfig.indent}{emote}"
        description = f"System: **{self.system_event.system_name}**\n"
        description += f"Minor Faction: **{self.system_event.minor_faction_name}**"
        embed = discord.Embed(title=title, description=description)

        return embed

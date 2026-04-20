import discord

from BotConfig.BotConfig import BotConfig
from Discord.View.SystemEventLog.SystemEventLogView import SystemEventLogView
from EventClass.SystemEvent.MinorFactionJoinSystemEvent import MinorFactionJoinSystemEvent

class MinorFactionJoinSystemEventLogView(SystemEventLogView):
    system_event: MinorFactionJoinSystemEvent

    def __init__(self, system_event: MinorFactionJoinSystemEvent):
        super().__init__(system_event)


    def get_embed(self):
        emote = BotConfig.emotes.minorFaction.state.expansion
        title = f"{emote}{BotConfig.indent}Minor Faction join System{BotConfig.indent}{emote}"
        description = f"System: **{self.system_event.system_name}**\n"
        description += f"Minor Faction: **{self.system_event.minor_faction_name}**"
        embed = discord.Embed(title=title, description=description)

        return embed

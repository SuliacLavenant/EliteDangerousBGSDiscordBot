import discord

from BotConfig.BotConfig import BotConfig
from Discord.View.SystemEventLog.SystemEventLogView import SystemEventLogView
from EventClass.SystemEvent.MinorFactionAcquireLeadershipSystemEvent import MinorFactionAcquireLeadershipSystemEvent

class MinorFactionAcquireLeadershipSystemEventLogView(SystemEventLogView):
    system_event: MinorFactionAcquireLeadershipSystemEvent

    def __init__(self, system_event: MinorFactionAcquireLeadershipSystemEvent):
        super().__init__(system_event)


    def get_embed(self):
        emote = f"{BotConfig.emotes.arrow.up} {BotConfig.emotes.minorFaction.positionInSystem.leader} {BotConfig.emotes.arrow.up}"
        title = f"{emote}{BotConfig.indent}Minor Faction Acquire System Leadership{BotConfig.indent}{emote}"
        description = f"System: **{self.system_event.system_name}**\n"
        description += f"Minor Faction: **{self.system_event.minor_faction_name}**\n"
        description += f"Old Leader: **{self.system_event.old_leader_minor_faction_name}**"
        embed = discord.Embed(title=title, description=description)

        return embed

import discord

from BotConfig.BotConfig import BotConfig
from Discord.View.SystemEventLog.SystemEventLogView import SystemEventLogView
from EventClass.SystemEvent.MinorFactionLoseLeadershipSystemEvent import MinorFactionLoseLeadershipSystemEvent

class MinorFactionLoseLeadershipSystemEventLogView(SystemEventLogView):
    system_event: MinorFactionLoseLeadershipSystemEvent

    def __init__(self, system_event: MinorFactionLoseLeadershipSystemEvent):
        super().__init__(system_event)


    def get_embed(self):
        emote = f"{BotConfig.emotes.arrow.down} {BotConfig.emotes.minorFaction.positionInSystem.other} {BotConfig.emotes.arrow.down}"
        title = f"{emote}{BotConfig.indent}Minor Faction Lost System Leadership{BotConfig.indent}{emote}"
        description = f"System: **{self.system_event.system_name}**\n"
        description += f"Minor Faction: **{self.system_event.minor_faction_name}**\n"
        description += f"New Leader: **{self.system_event.new_leader_minor_faction_name}**"
        embed = discord.Embed(title=title, description=description)

        return embed

import discord
import urllib.parse

from EventClass.SystemEvent.SystemEvent import SystemEvent

class SystemEventLogView(discord.ui.View):
    system_event: SystemEvent

    def __init__(self, system_event: SystemEvent):
        super().__init__()
        self.system_event = system_event

        self.add_item(discord.ui.Button(
            label="Inara",
            url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system_event.system_name)}",
            emoji="🌐",
            row=0
        ))


    def get_embed(self):
        title = "System Event"
        description = ""
        embed = discord.Embed(title=title, description=description)

        return embed

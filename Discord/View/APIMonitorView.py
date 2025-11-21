import discord

class APIMonitorView(discord.ui.View):
    onlineEmote: str = ":green_circle:"
    offlineEmote: str = ":red_circle:"

    def __init__(self, aPIStatus: dict):
        super().__init__()
        self.aPIStatus = aPIStatus


    def getEmbed(self):
        title = "API Monitor"
        description = ""

        for api in self.aPIStatus.values():
            description += self.getAPIRecapLine(api)

        embed = discord.Embed(title=title, description=description)

        return embed

    def getAPIRecapLine(self, api: dict):
        line = self.getOnlineEmote(api)+f" {api["name"]}"
        if not api["online"]:
            line += f", Issue: {api["issue"]}"
        line += "\n"
        return line

    def getOnlineEmote(self, api: dict):
        if api["online"]:
            return self.onlineEmote
        else:
            return self.offlineEmote

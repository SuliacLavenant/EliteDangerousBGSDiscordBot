import discord
import urllib.parse

#custom
from DataClass.MinorFaction import MinorFaction

class MinorFactionView(discord.ui.View):
    def __init__(self, minorFaction: MinorFaction):
        super().__init__()
        self.minorFaction = minorFaction

        if self.minorFaction != None:
            self.add_item(discord.ui.Button(
                label="Inara",
                url=f"https://inara.cz/elite/minorfaction/?search={urllib.parse.quote(self.minorFaction.name)}",
                emoji="🌐"
            ))

    def getEmbed(self):
        if self.minorFaction == None:
            return self.getNoMinorFactionEmbed()
        else:
            return self.getFactionRecapEmbed()


    def getNoMinorFactionEmbed(self):
        embed = discord.Embed(
            title="No Minor Faction Set",
            description="Please set a Minor Faction"
        )
        return embed


    def getFactionRecapEmbed(self):
        title = self.minorFaction.name.title()
        description = f"Allegiance: **{self.minorFaction.allegiance.title()}**\n"
        description += f"Government: **{self.minorFaction.government.title()}**"
        embed = discord.Embed(title=title, description=description)

        embed.add_field(name=f"Systems", value=f"Present in **{self.minorFaction.numberOfSystems}** systems. \n Controlling **TBA** systems.", inline=True)

        return embed

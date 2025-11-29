import discord
import urllib.parse

#custom
from BotConfig import BotConfig

class SystemsRecapLegendView(discord.ui.View):


    def __init__(self, minorFactionName: str):
        super().__init__()
        self.title = "Recap Legend"
        self.minorFactionName = minorFactionName.title()


    def getEmbed(self):
        description=""
        embed = discord.Embed(title=self.title, description=description)

        #status
        status = f"{BotConfig.emotes["warningLevel0"]}: {self.minorFactionName} is leader with a {int(BotConfig.leaderInfluenceWarning["level1"]*100)}% margin.\n"
        status += f"{BotConfig.emotes["warningLevel1"]}: {self.minorFactionName} is leader with a {int(BotConfig.leaderInfluenceWarning["level2"]*100)}%-{int(BotConfig.leaderInfluenceWarning["level1"]*100)}% margin.\n"
        status += f"{BotConfig.emotes["warningLevel2"]}: {self.minorFactionName} is leader with a {int(BotConfig.leaderInfluenceWarning["level3"]*100)}%-{int(BotConfig.leaderInfluenceWarning["level2"]*100)}% margin.\n"
        status += f"{BotConfig.emotes["warningLevel3"]}: {self.minorFactionName} is leader with less than a {int(BotConfig.leaderInfluenceWarning["level3"]*100)}% margin.\n"
        status += f"{BotConfig.emotes["warningLevelOther"]}: {self.minorFactionName} have no specific status in this System (not leader and not in retreat).\n"
        status += f"{BotConfig.emotes["retreat"]}: {self.minorFactionName} is retreating from this System."
        embed.add_field(name=f"Status Indication", value=status, inline=False)

        #position in system
        position = f"{BotConfig.emotes["leader"]}: {self.minorFactionName} is leader of the System.\n"
        position += f"{BotConfig.emotes["noLeader"]}: {self.minorFactionName} is in the System."
        embed.add_field(name=f"Position in System", value=position, inline=False)

        #number of faction in system
        number = f"{BotConfig.emotes["minimumFaction"]}: Minimum of Minor Factions in this System, {self.minorFactionName} can't be retreated.\n"
        number += ":number_4::number_5::number_6:" + ": Number of factions in System.\n"
        number += f"{BotConfig.emotes["maximumFaction"]}: Maximum of Minor Factions in this System, no other {self.minorFactionName} can expend into this System."
        embed.add_field(name=f"Number of faction", value=number, inline=False)

        return embed

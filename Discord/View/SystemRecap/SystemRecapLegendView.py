import discord
import urllib.parse

#custom
from BotConfig.BotConfig import BotConfig

class SystemsRecapLegendView(discord.ui.View):


    def __init__(self, minorFactionName: str):
        super().__init__()
        self.title = "Recap Legend"
        self.minorFactionName = minorFactionName.title()


    def getEmbed(self):
        description=""
        embed = discord.Embed(title=self.title, description=description)

        #status Warning Indicator
        status = f"{BotConfig.emotes["warningLevel0"]}: **{self.minorFactionName}** is leader with a **{int(BotConfig.leaderInfluenceWarning["level1"]*100)}%** margin.\n"
        status += f"{BotConfig.emotes["warningLevel1"]}: **{self.minorFactionName}** is leader with a **{int(BotConfig.leaderInfluenceWarning["level2"]*100)}%**-**{int(BotConfig.leaderInfluenceWarning["level1"]*100)}%** margin.\n"
        status += f"{BotConfig.emotes["warningLevel2"]}: **{self.minorFactionName}** is leader with a **{int(BotConfig.leaderInfluenceWarning["level3"]*100)}%**-**{int(BotConfig.leaderInfluenceWarning["level2"]*100)}%** margin.\n"
        status += f"{BotConfig.emotes["warningLevel3"]}: **{self.minorFactionName}** is leader with less than a **{int(BotConfig.leaderInfluenceWarning["level3"]*100)}%** margin.\n"
        status += f"{BotConfig.emotes["warningImportantState"]}: **{self.minorFactionName}** have an Important state (conflict or retreat).\n"
        status += f"{BotConfig.emotes["warningExpansion"]}: **{self.minorFactionName}** is close to trigger an **Expansion** (influence>**{int(BotConfig.influenceExpansionWarning*100)}%**, **75%** to trigger an **Expansion**).\n"
        status += f"{BotConfig.emotes["warningLevelOther"]}: **{self.minorFactionName}** have no specific status in this System (not leader and not in retreat)."
        embed.add_field(name=f"Status Warning Indicator", value=status, inline=False)

        #important State
        importantState = f"{BotConfig.emotesN.minorFaction.state.war}: **{self.minorFactionName}** is engaged in a **War** or a **Civil War**.\n"
        importantState += f"{BotConfig.emotesN.minorFaction.state.election}: **{self.minorFactionName}** is engaged in an **Election**.\n"
        importantState += f"{BotConfig.emotesN.minorFaction.state.retreat}: **{self.minorFactionName}** is in **Retreat**.\n"
        importantState += f"{BotConfig.emotesN.minorFaction.state.expansion}: **{self.minorFactionName}** is in **Expansion**. (not implemented yet)\n"
        importantState += f"{BotConfig.emotesN.minorFaction.state.none}: **{self.minorFactionName}** does not have an important state."
        embed.add_field(name=f"Important State", value=importantState, inline=False)

        #position in system
        position = f"{BotConfig.positionInSystemEmotes["leader"]}: **{self.minorFactionName}** is **Leader**.\n"
        position += f"{BotConfig.positionInSystemEmotes["other"]}: **{self.minorFactionName}** is **present**."
        embed.add_field(name=f"Position in System", value=position, inline=False)

        #number of faction in system
        number = f"{BotConfig.numberOfFactionEmotes["minimumFaction"]}: **Minimum** of Minor Factions, **{self.minorFactionName}** can't be retreated.\n"
        number += ":number_4::number_5::number_6:" + ": **Number** of Minor Factions.\n"
        number += f"{BotConfig.numberOfFactionEmotes["maximumFaction"]}: **Maximum** of Minor Factions, no other Minor Factions can expand into this System."
        embed.add_field(name=f"Number of faction", value=number, inline=False)

        return embed

import discord
from discord.ext import commands
from discord import app_commands

from SystemInfoMinorFactionFocused import SystemInfoMinorFactionFocused

INARASYSTEMPAGE = "https://inara.cz/elite/starsystem/?search="

class BGSManagementBot(commands.Bot):
    async def on_ready(self):
        print("bot online")

        try:
            guild = discord.Object(id=281470136551079936)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commandes to guild {guild.id}")
        
        except Exception as e:
            print(f"Error syncing commands: {e}")

    def getSystemMinorFactionRecapEmbed(self, systemInfoMinorFaction: SystemInfoMinorFactionFocused):
        title = systemInfoMinorFaction.systemName
        if systemInfoMinorFaction.controllingFaction == systemInfoMinorFaction.minorFactionName:
            title += "   :crown:"

        description = f"**Leader**: [{systemInfoMinorFaction.controllingFaction}]({systemInfoMinorFaction.controllingFactionInaraLink}), "
        description += "        "
        description += f"**Influence**: {round(systemInfoMinorFaction.controllingFactionInfluence*100,1)}%"

        systemRecapEmbed = discord.Embed(title=title, url=INARASYSTEMPAGE+systemInfoMinorFaction.systemName, description=description)

        if systemInfoMinorFaction.controllingFaction != systemInfoMinorFaction.minorFactionName:
            systemRecapEmbed.add_field(name=f"{systemInfoMinorFaction.minorFactionName} Influence", value=round(systemInfoMinorFaction.influence*100,1), inline=False)

        systemRecapEmbed.add_field(name="Population", value=systemInfoMinorFaction.populationStr, inline=True)
        systemRecapEmbed.add_field(name="Current State(s)", value="TODO", inline=False)

        #systemRecapEmbed.add_field(name="Influence Since Yesterday", value="", inline=True)
        #systemRecapEmbed.add_field(name="Influence Since Last Week", value="", inline=True)
        #systemRecapEmbed.add_field(name="", value="", inline=True)
        systemRecapEmbed.set_footer(text=f"Info updated: {systemInfoMinorFaction.dateStr}")

        return systemRecapEmbed


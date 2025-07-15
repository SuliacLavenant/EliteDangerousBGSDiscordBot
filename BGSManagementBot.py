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
        systemRecapEmbed = discord.Embed(title=systemInfoMinorFaction.systemName, url=INARASYSTEMPAGE+systemInfoMinorFaction.systemName)
        systemRecapEmbed.add_field(name="Current Influence", value=systemInfoMinorFaction.influence, inline=False)
        systemRecapEmbed.add_field(name="Current State(s)", value="TODO", inline=False) 

        systemRecapEmbed.add_field(name="Influence Since Yesterday", value="", inline=True)
        systemRecapEmbed.add_field(name="Influence Since Last Week", value="", inline=True)
        #systemRecapEmbed.add_field(name="", value="", inline=True)
        systemRecapEmbed.set_footer(text=f"Info updated: {systemInfoMinorFaction.dateStr}")

        return systemRecapEmbed


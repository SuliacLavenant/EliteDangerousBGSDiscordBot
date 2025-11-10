import discord
from discord.ext import commands
from discord import app_commands

from DataClass.SystemMinorFactionRecap import SystemMinorFactionRecap

from View.SystemsRecapView import SystemsRecapView

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

    def getSystemsMinorFactionRecapEmbeds(self, systemsRecap: dict):
        systemsName = list(systemsRecap.keys())
        systemsName.sort()

        embeds=[]
        systems = {}
        for systemName in systemsName:
            systems[systemName] = systemsRecap[systemName]
            if len(systems)>=20:
                embeds.append(SystemsRecapView("test", systems).getEmbed())
                systems = {}
        if len(systems)>0:
            embeds.append(SystemsRecapView("test", systems).getEmbed())

        
        return embeds


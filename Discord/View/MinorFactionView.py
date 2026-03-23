import discord
import urllib.parse

from DataClass.MinorFaction import MinorFaction
from DataClass.GuildSettings import GuildSettings
from DataStorageManager import DataStorageManager
from Discord.Modal.SetMinorFactionModal import SetMinorFactionModal
from Discord.View.MinorFactionSharedSystemsView import MinorFactionSharedSystemsView


class MinorFactionView(discord.ui.View):
    minor_faction: MinorFaction
    guild_settings: GuildSettings
    shared_system_names: list = None

    def __init__(self, minor_faction: MinorFaction, guild_id: int):
        super().__init__()
        self.minor_faction = minor_faction
        self.guild_id = guild_id
        self.guild_settings = DataStorageManager.get_guild_settings(guild_id)
        if self.guild_settings.minor_faction_name != None:
            self.guild_minor_faction = DataStorageManager.get_minor_faction(self.guild_id, self.guild_settings.minor_faction_name.lower())
            self.shared_system_names = self.minor_faction.get_shared_system_names(self.guild_minor_faction)

        if self.minor_faction != None:
            self.add_item(discord.ui.Button(
                label="Inara",
                url=f"https://inara.cz/elite/minorfaction/?search={urllib.parse.quote(self.minor_faction.name)}",
                emoji="🌐"
            ))

    
    @discord.ui.button(label="Show shared systems", style=discord.ButtonStyle.primary, row=2)
    async def show_shared_systems(self, button: discord.ui.Button, interaction: discord.Interaction):
        if True: #permission
            systems = []
            for shared_system_name in self.shared_system_names:
                systems.append(DataStorageManager.get_system(self.guild_id,shared_system_name))
            
            view = MinorFactionSharedSystemsView(systems,self.minor_faction,self.guild_minor_faction)
            await interaction.response.send_message(embed=view.getEmbed(), view=view)
            #await interaction.followup.send("Autre message")
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def getEmbed(self):
        title = self.minor_faction.name.title()
        description = f"Allegiance: **{self.minor_faction.allegiance.title()}**\n"
        description += f"Government: **{self.minor_faction.government.title()}**\n"
        if self.minor_faction.origin_system_name != "" and self.minor_faction.origin_system_name != None:
            description += f"Origin System: [**{self.minor_faction.origin_system_name.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.minor_faction.origin_system_name)})\n"
        if self.shared_system_names != None:
            description += f"Shared system: {len(self.shared_system_names)}\n"
        embed = discord.Embed(title=title, description=description)
        return embed

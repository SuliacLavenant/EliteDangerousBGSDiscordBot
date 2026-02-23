import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from DataClass.System import System
from DataClass.GuildSettings import GuildSettings
from DataClass.Mission.SystemMission.RetreatMinorFactionFromSystemMission import RetreatMinorFactionFromSystemMission
from PermissionManager.PermissionManager import PermissionManager

from Discord.Modal.System.SetSystemArchitectModal import SetSystemArchitectModal
from Discord.Modal.Mission.CreateRetreatMinorFactionFromSystemMissionModal import CreateRetreatMinorFactionFromSystemMissionModal

class SystemView(discord.ui.View):
    def __init__(self, system: System, guildSettings: GuildSettings):
        super().__init__()
        self.system = system
        self.guildSettings = guildSettings

        
        self.add_item(discord.ui.Button(
            label="Inara",
            url=f"https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.system.name)}",
            emoji="🌐",
            row=0
        ))

        if self.system.isStored:
            if self.system.isArchitected == None:
                setArchitectButton = discord.ui.Button(
                    label="Set Architect",
                    style=discord.ButtonStyle.secondary,
                    emoji="🏗️",
                    row=1
                )
                setArchitectButton.callback = self.setArchitectButtonCallback
                self.add_item(setArchitectButton)

                setNativeSystemtButton = discord.ui.Button(
                    label="Native System",
                    style=discord.ButtonStyle.secondary,
                    emoji="🏛️",
                    row=1
                )
                setNativeSystemtButton.callback = self.setNativeSystemtButtonCallback
                self.add_item(setNativeSystemtButton)


    async def setArchitectButtonCallback(self, interaction: discord.Interaction):
        setSystemArchitectModal = SetSystemArchitectModal(self.system)
        await interaction.response.send_modal(setSystemArchitectModal)
        await setSystemArchitectModal.wait()

        system = DataStorageManager.get_system(interaction.guild_id,self.system.name)
        systemView = SystemView(system, self.guildSettings)
        await interaction.edit_original_response(view=systemView,embed=systemView.getEmbed())


    async def setNativeSystemtButtonCallback(self, interaction: discord.Interaction):
        system = DataStorageManager.get_system(interaction.guild_id,self.system.name)
        system.isArchitected = False

        DataStorageManager.store_system(interaction.guild_id,system)

        systemView = SystemView(system, self.guildSettings)
        await interaction.response.edit_message(view=systemView,embed=systemView.getEmbed())


    @discord.ui.button(label="Create Retreat Mission", style=discord.ButtonStyle.primary, row=2)
    async def create_mission(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.mission_permissions.create(interaction.user.id):
            create_retreat_minor_faction_from_system_mission_modal = CreateRetreatMinorFactionFromSystemMissionModal(self.system)
            await interaction.response.send_modal(create_retreat_minor_faction_from_system_mission_modal)
            await create_retreat_minor_faction_from_system_mission_modal.wait()
            
            minor_faction_name = create_retreat_minor_faction_from_system_mission_modal.minor_faction
            if minor_faction_name != None:
                mission = RetreatMinorFactionFromSystemMission(minor_faction_name=minor_faction_name,system_name=self.system.name)
                DataStorageManager.store_mission(interaction.guild_id,mission)

            system_view = SystemView(self.system, self.guildSettings)
            await interaction.message.edit(view=system_view,embed=system_view.getEmbed())
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def getEmbed(self):
        title = self.system.name.title()
        if self.system.isStored:
            title += f" {BotConfig.emotesN.data.saved}"
        else:
            title += f" {BotConfig.emotesN.data.online}"

        description = f"{BotConfig.emotesN.system.information.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotesN.system.information.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotesN.system.information.security} Security Level: **{self.system.security.title()}**\n"
        description += f"{self.getNumberMinorFactionEmote(self.system)} Number of Minor Factions: **{len(self.system.minor_factions_names)}**\n"
        if self.system.isArchitected:
            description += f"{BotConfig.emotesN.system.information.architect} Architect: **{self.system.architect.title()}**\n"
        description += "."

        embed = discord.Embed(title=title, description=description)

        ranking = self.system.get_minor_factions_ranking()
        current = 1
        while current<=len(ranking):
            minor_faction = self.system.minor_factions[ranking[current]]
            minorFactionDescription = f"Allegiance: **{minor_faction.allegiance.title()}**\n"
            minorFactionDescription += f"Government: **{minor_faction.government.title()}**\n"

            emote = ""
            if current == 1:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.leader
            else:
                emote = BotConfig.emotesN.minorFaction.positionInSystem.other

            title = f"{emote} {minor_faction.name} {emote} - < {round(self.system.minor_factions_influence[minor_faction.name.lower()]*100,1)}% >"
            if minor_faction.name.lower() == self.guildSettings.minor_faction_name:
                title += f" {BotConfig.emotesN.pin}"

            embed.add_field(name=title, value=minorFactionDescription, inline=False)

            current+=1

        return embed

    def getNumberMinorFactionEmote(self, system: System):
        if len(system.minor_factions_names)<=3:
            return BotConfig.emotesN.system.numberOfMinorFaction[3]
        elif len(system.minor_factions_names)>=7:
            return BotConfig.emotesN.system.numberOfMinorFaction[7]
        else:
            return BotConfig.emotesN.system.numberOfMinorFaction[len(system.minor_factions_names)]

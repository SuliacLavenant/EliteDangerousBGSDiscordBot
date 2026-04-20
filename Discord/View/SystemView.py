import discord
import urllib.parse

from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from DataStorageManager import DataStorageManager
from DataClass.System import System
from DataClass.GuildSettings import GuildSettings
from DataClass.Mission.MissionProgressEnum import MissionProgressEnum
from DataClass.Mission.SystemMission.RetreatMinorFactionFromSystemMission import RetreatMinorFactionFromSystemMission
from DataClass.Mission.SystemMission.SetMinorFactionAsLeaderInSystemMission import SetMinorFactionAsLeaderInSystemMission
from PermissionManager.PermissionManager import PermissionManager

from Discord.Modal.System.SetSystemArchitectModal import SetSystemArchitectModal
from Discord.Modal.Mission.CreateRetreatMinorFactionFromSystemMissionModal import CreateRetreatMinorFactionFromSystemMissionModal
from Discord.Modal.Mission.CreateSetMinorFactionAsLeaderInSystemMissionModal import CreateSetMinorFactionAsLeaderInSystemMissionModal
class SystemView(discord.ui.View):
    is_for_trusted_channel: bool = False

    def __init__(self, system: System, guildSettings: GuildSettings, is_for_trusted_channel: bool = False):
        super().__init__()
        self.system: System = system
        self.guildSettings: GuildSettings = guildSettings

        self.is_for_trusted_channel: bool = is_for_trusted_channel

        
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
        system_view = SystemView(system, self.guildSettings, self.is_for_trusted_channel)
        await interaction.message.edit(view=system_view,embeds=system_view.get_embeds())


    async def setNativeSystemtButtonCallback(self, interaction: discord.Interaction):
        system = DataStorageManager.get_system(interaction.guild_id,self.system.name)
        system.isArchitected = False

        DataStorageManager.store_system(interaction.guild_id,system)

        system_view = SystemView(system, self.guildSettings, self.is_for_trusted_channel)
        await interaction.message.edit(view=system_view,embeds=system_view.get_embeds())


    @discord.ui.button(label="Create Retreat Mission", style=discord.ButtonStyle.primary, row=2)
    async def create_retreat_mission(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.mission_permissions.create(interaction.user.id):
            create_retreat_minor_faction_from_system_mission_modal = CreateRetreatMinorFactionFromSystemMissionModal(self.system)
            await interaction.response.send_modal(create_retreat_minor_faction_from_system_mission_modal)
            await create_retreat_minor_faction_from_system_mission_modal.wait()
            
            minor_faction_name = create_retreat_minor_faction_from_system_mission_modal.minor_faction
            if minor_faction_name != None:
                mission = RetreatMinorFactionFromSystemMission(minor_faction_name=minor_faction_name,system_name=self.system.name)
                DataStorageManager.store_mission(interaction.guild_id,mission)

                self.system = DataStorageManager.get_system(interaction.guild_id, self.system.name)
                self.system.add_mission(mission.mission_id)
                DataStorageManager.store_system(interaction.guild_id, self.system)

            system_view = SystemView(self.system, self.guildSettings, self.is_for_trusted_channel)
            await interaction.message.edit(view=system_view,embeds=system_view.get_embeds())
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    @discord.ui.button(label="Create Set Leader Mission", style=discord.ButtonStyle.primary, row=2)
    async def create_set_leader_mission(self, button: discord.ui.Button, interaction: discord.Interaction):
        if PermissionManager.mission_permissions.create(interaction.user.id):
            create_set_minor_faction_as_leader_in_system_mission_modal = CreateSetMinorFactionAsLeaderInSystemMissionModal(self.system)
            await interaction.response.send_modal(create_set_minor_faction_as_leader_in_system_mission_modal)
            await create_set_minor_faction_as_leader_in_system_mission_modal.wait()
            
            minor_faction_name = create_set_minor_faction_as_leader_in_system_mission_modal.minor_faction
            if minor_faction_name != None:
                mission = SetMinorFactionAsLeaderInSystemMission(minor_faction_name=minor_faction_name,system_name=self.system.name)
                DataStorageManager.store_mission(interaction.guild_id,mission)

                self.system = DataStorageManager.get_system(interaction.guild_id, self.system.name)
                self.system.add_mission(mission.mission_id)
                DataStorageManager.store_system(interaction.guild_id, self.system)

            system_view = SystemView(self.system, self.guildSettings, self.is_for_trusted_channel)
            await interaction.message.edit(view=system_view,embeds=system_view.get_embeds())
        else:
            await interaction.response.send_message(f"You don't have the permission to do this.", ephemeral=True)


    def getEmbed(self):
        title = self.system.name.title()
        if self.system.isStored:
            title += f" {BotConfig.emotes.data.saved}"
        else:
            title += f" {BotConfig.emotes.data.online}"

        description = f"{BotConfig.emotes.system.information.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotes.system.information.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotes.system.information.security} Security Level: **{self.system.security.title()}**\n"
        description += f"{self.getNumberMinorFactionEmote(self.system)} Number of Minor Factions: **{len(self.system.minor_factions_names)}**\n"
        if self.system.isArchitected:
            description += f"{BotConfig.emotes.system.information.architect} Architect: **{self.system.architect.title()}**\n"
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
                emote = BotConfig.emotes.minorFaction.positionInSystem.leader
            else:
                emote = BotConfig.emotes.minorFaction.positionInSystem.other

            title = f"{emote} {minor_faction.name} {emote} - < {round(self.system.minor_factions_influence[minor_faction.name.lower()]*100,1)}% >"
            if minor_faction.name.lower() == self.guildSettings.minor_faction_name:
                title += f" {BotConfig.emotes.pin}"

            embed.add_field(name=title, value=minorFactionDescription, inline=False)

            current+=1

        return embed
    

    def get_embeds(self):
        embeds = []
        title = self.system.name.title()
        if self.system.isStored:
            title += f" {BotConfig.emotes.data.saved}"
        else:
            title += f" {BotConfig.emotes.data.online}"

        description = f"{BotConfig.emotes.system.information.economy} Economy: **{self.system.getStrSystemEconomy()}**\n"
        description += f"{BotConfig.emotes.system.information.population} Population: **{self.system.getStrSystemPopulation()}**\n"
        description += f"{BotConfig.emotes.system.information.security} Security Level: **{self.system.security.title()}**\n"
        description += f"{self.getNumberMinorFactionEmote(self.system)} Number of Minor Factions: **{len(self.system.minor_factions_names)}**\n"
        if self.system.isArchitected:
            description += f"{BotConfig.emotes.system.information.architect} Architect: **{self.system.architect.title()}**\n"
        description += f"{BotConfig.indent2}"

        embed = discord.Embed(title=title, description=description)
        embeds.append(embed)

        ranking = self.system.get_minor_factions_ranking()
        current = 1
        while current<=len(ranking):
            minor_faction = self.system.minor_factions[ranking[current]]
            minorFactionDescription = f"{BotConfig.indent2} Allegiance: **{minor_faction.allegiance.title()}**\n"
            minorFactionDescription += f"{BotConfig.indent2} Government: **{minor_faction.government.title()}**\n"

            emote = ""
            if current == 1:
                emote = BotConfig.emotes.minorFaction.positionInSystem.leader
            else:
                emote = BotConfig.emotes.minorFaction.positionInSystem.other

            title = f"{emote} {minor_faction.name} {emote} - < {round(self.system.minor_factions_influence[minor_faction.name.lower()]*100,1)}% >"
            if minor_faction.name.lower() == self.guildSettings.minor_faction_name:
                title += f" {BotConfig.emotes.pin}"

            embed.add_field(name=title, value=minorFactionDescription, inline=False)

            current+=1

        #missions
        if self.is_for_trusted_channel and len(self.system.mission_ids)>0:
            embed = discord.Embed(title="Missions")
            embeds.append(embed)

            for mission_id in self.system.mission_ids:
                mission = DataStorageManager.get_mission(self.guildSettings.guild_id, mission_id)
                title = ""
                details = ""
                if mission.mission_type == "SetMinorFactionAsLeaderInSystemMission":
                    title = f"{BotConfig.emotes.minorFaction.positionInSystem.leader} Set Leader {BotConfig.emotes.minorFaction.positionInSystem.leader}"
                    mission.update_with_system_data(self.system)
                    mission.check_mission_state()
                    details += f"{BotConfig.indent2}{BotConfig.emotes.mission.state.state} State: {mission.get_mission_state_emote()} **{mission.state.value}** \n"
                    details += f"{BotConfig.indent2}{BotConfig.emotes.target} Target: **{mission.minor_faction_name}** \n"
                    if mission.current_influence_difference<0:
                        details += f"{BotConfig.indent2}{BotConfig.emotes.minorFaction.influence.up} Missing Influence: {mission.get_target_minor_faction_influence_difference_string()} \n"
                    elif mission.conflict != None:
                        details += f"{BotConfig.indent2}{BotConfig.emotes.minorFaction.state.war} Conflict: {mission.conflict} \n"
                    
                elif mission.mission_type == "RetreatMinorFactionFromSystemMission":
                    title = f"{BotConfig.emotes.minorFaction.state.retreat} Retreat {BotConfig.emotes.minorFaction.state.retreat}"
                    mission.update_with_system_data(self.system)
                    mission.check_mission_state()
                    details += f"{BotConfig.indent2}{BotConfig.emotes.mission.state.state} State: {mission.get_mission_state_emote()} **{mission.state.value}** \n"
                    details += f"{BotConfig.indent2}{BotConfig.emotes.target} Target: **{mission.minor_faction_name}** \n"
                    details += f"{BotConfig.indent2}{BotConfig.emotes.minorFaction.influence.down} Current Influence: {mission.get_current_influence_string()} \n"

                embed.add_field(name=title, value=details, inline=False)


        return embeds


    def getNumberMinorFactionEmote(self, system: System):
        if len(system.minor_factions_names)<=3:
            return BotConfig.emotes.system.numberOfMinorFaction[3]
        elif len(system.minor_factions_names)>=7:
            return BotConfig.emotes.system.numberOfMinorFaction[7]
        else:
            return BotConfig.emotes.system.numberOfMinorFaction[len(system.minor_factions_names)]


    def get_mission_state_emote(self, mission):
        match mission.state:
            case MissionProgressEnum.UPCOMING:
                return BotConfig.emotes.mission.state.upcoming
            case MissionProgressEnum.ACTIVE:
                return BotConfig.emotes.mission.state.active
            case MissionProgressEnum.PENDING:
                return BotConfig.emotes.mission.state.pending
            case MissionProgressEnum.COMPLETE:
                return BotConfig.emotes.mission.state.complete
            case _:
                return "None"
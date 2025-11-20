import discord
from discord.ext import commands
from discord import app_commands

#custom
from DataManager import DataManager
from View.SystemGroup.CreateSystemGroupModal import CreateSystemGroupModal
from DataClass.SystemGroup import SystemGroup

class ManageSystemGroupView(discord.ui.View):
    def __init__(self, systemGroups):
        super().__init__()
        self.systemGroups = systemGroups
        print(systemGroups)


    @discord.ui.button(label="Create New Group", style=discord.ButtonStyle.primary)
    async def CreateNewGroup(self, interaction: discord.Interaction, button: discord.ui.Button):
        createSystemGroupModal = CreateSystemGroupModal()
        await interaction.response.send_modal(createSystemGroupModal)
        await createSystemGroupModal.wait()
        groupName = str(createSystemGroupModal.groupName)
        if DataManager.getSystemGroup(interaction.guild_id, groupName) == None:
            systemGroup = SystemGroup(name=groupName)
            DataManager.createSystemGroup(interaction.guild_id, systemGroup)
            
            self.clear_items()
            await interaction.edit_original_response(embed=self.getGroupCreatedEmbed(systemGroup), view=self)
        else:
            self.clear_items()
            await interaction.edit_original_response(embed=self.getGroupAlreadyExistEmbed(groupName), view=self)


    def getEmbed(self):
        title = "Manage System Groups"
        description = f"Number of Groups: {len(self.systemGroups)}"
        embed = discord.Embed(title=title, description=description)

        for systemGroup in self.systemGroups:
            embed.add_field(name=systemGroup.name, value="system list TODO", inline=True)

        return embed


    def getGroupCreatedEmbed(self, systemGroup: SystemGroup):
        title = f"Create System Group \"{systemGroup.name}\""
        description = "Group Created!"
        embed = discord.Embed(title=title, description=description)
        return embed


    def getGroupAlreadyExistEmbed(self, systemGroupName: str):
        title = f"Create System Group \"{systemGroupName}\""
        description = "Group already exist"
        embed = discord.Embed(title=title, description=description)
        return embed


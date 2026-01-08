import discord

#custom
from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from Discord.Modal.CreateSystemGroupModal import CreateSystemGroupModal
from Discord.View.SystemGroup.Edit.SelectSystemGroupToEditView import SelectSystemGroupToEditView

from DataClass.SystemGroup import SystemGroup

class ManageSystemGroupsView(discord.ui.View):
    def __init__(self, systemGroups):
        super().__init__()
        self.systemGroups = systemGroups
        print(systemGroups)


    @discord.ui.button(label="Create New Group", style=discord.ButtonStyle.success)
    async def CreateNewGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        createSystemGroupModal = CreateSystemGroupModal()
        await interaction.response.send_modal(createSystemGroupModal)
        await createSystemGroupModal.wait()
        groupName = str(createSystemGroupModal.systemGroupName.value)
        if DataManager.getSystemGroup(interaction.guild_id, groupName) == None:
            systemGroup = SystemGroup(name=groupName)
            DataManager.saveSystemGroup(interaction.guild_id, systemGroup)
            
            self.clear_items()
            await interaction.edit_original_response(embed=self.getGroupCreatedEmbed(systemGroup), view=self)
        else:
            self.clear_items()
            await interaction.edit_original_response(embed=self.getGroupAlreadyExistEmbed(groupName), view=self)


    @discord.ui.button(label="Edit System Group", style=discord.ButtonStyle.secondary)
    async def editSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        selectSystemGroupToEditView = SelectSystemGroupToEditView(self.systemGroups)

        await interaction.response.edit_message(embed=selectSystemGroupToEditView.getEmbed(),view=selectSystemGroupToEditView)


    def getEmbed(self):
        title = "Manage System Groups"
        description = f"Number of Groups: {len(self.systemGroups)}"
        embed = discord.Embed(title=title, description=description)

        for systemGroup in self.systemGroups:
            embed.add_field(name=systemGroup.name, value=f"{BotConfig.emotesN.systems} {len(systemGroup.systems)} systems", inline=False)

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


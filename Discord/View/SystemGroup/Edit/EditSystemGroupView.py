import discord

#custom
from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup
from Discord.View.SystemGroup.Edit.SystemGroupDeletedView import SystemGroupDeletedView
from Discord.View.SystemGroup.Edit.SelectSystemsToAddToGroupView import SelectSystemsToAddToGroupView
from Discord.Modal.SystemGroup.Edit.DeleteSystemGroupConfirmationModal import DeleteSystemGroupConfirmationModal

class EditSystemGroupView(discord.ui.View):
    def __init__(self, systemGroup: str):
        super().__init__()
        self.systemGroup = systemGroup

    @discord.ui.button(label="Add Systems to SystemGroup", style=discord.ButtonStyle.secondary, row=0)
    async def addSystemsToSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        systemNameList = DataManager.getSystemNamesWithNoGroupList(interaction.guild_id)
        systemNameList.sort()
        if systemNameList!=None and len(systemNameList)>0:
            selectSystemsToAddToGroupView = SelectSystemsToAddToGroupView(self.systemGroup,systemNameList)
            await interaction.response.edit_message(embed=selectSystemsToAddToGroupView.getEmbed(),view=selectSystemsToAddToGroupView)
        else:
            editSystemGroupView = EditSystemGroupView(self.systemGroup)
            await interaction.response.edit_message(embed=editSystemGroupView.getEmbed(),view=editSystemGroupView)

    @discord.ui.button(label="Delete System Group", style=discord.ButtonStyle.danger, row=1)
    async def deleteSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        deleteSystemGroupConfirmationModal = DeleteSystemGroupConfirmationModal(self.systemGroup.name)
        await interaction.response.send_modal(deleteSystemGroupConfirmationModal)
        await deleteSystemGroupConfirmationModal.wait()

        if deleteSystemGroupConfirmationModal.systemGroupNameInput.value == self.systemGroup.name:
            DataManager.removeSystemGroup(interaction.guild_id,self.systemGroup.name)
            systemGroupDeletedView = SystemGroupDeletedView(self.systemGroup.name)
            await interaction.message.edit(embed=systemGroupDeletedView.getEmbed(),view=systemGroupDeletedView)
        else:
            await interaction.message.edit(embed=self.getEmbed(),view=self)

    def getEmbed(self):
        description="Systems:"
        for systemName in self.systemGroup.systems:
                description += f"\n{systemName}"
        embed = discord.Embed(
            title=f"Edit System Group: {self.systemGroup.name}",
            description=description
            
        )
        return embed

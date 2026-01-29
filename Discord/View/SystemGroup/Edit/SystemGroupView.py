import discord

#custom
from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup
from Discord.View.SystemGroup.Edit.SelectSystemsToAddToGroupView import SelectSystemsToAddToGroupView
from Discord.Modal.SystemGroup.Edit.DeleteSystemGroupConfirmationModal import DeleteSystemGroupConfirmationModal
from Discord.Modal.SystemGroup.SetEmoteForSystemGroupModal import SetEmoteForSystemGroupModal
from DataStorageManager import DataStorageManager

class SystemGroupView(discord.ui.View):
    def __init__(self, systemGroup: SystemGroup):
        super().__init__()
        self.systemGroup = systemGroup

    @discord.ui.button(label="Set Emote For System Group", style=discord.ButtonStyle.secondary, emoji="🙂", row=0)
    async def setEmoteForSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        setEmoteForSystemGroupModal = SetEmoteForSystemGroupModal(self.systemGroup)
        await interaction.response.send_modal(setEmoteForSystemGroupModal)
        await setEmoteForSystemGroupModal.wait()

        systemGroupView = SystemGroupView(DataStorageManager.getSystemGroup(interaction.guild_id,self.systemGroup.name))
        await interaction.message.edit(embed=systemGroupView.getEmbed(),view=systemGroupView)
    

    @discord.ui.button(label="Add Systems to SystemGroup", style=discord.ButtonStyle.secondary, row=1)
    async def addSystemsToSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        systemNameList = DataManager.getSystemNamesWithNoGroupList(interaction.guild_id)
        systemNameList.sort()
        if systemNameList!=None and len(systemNameList)>0:
            selectSystemsToAddToGroupView = SelectSystemsToAddToGroupView(self.systemGroup,systemNameList)
            await interaction.response.edit_message(embed=selectSystemsToAddToGroupView.getEmbed(),view=selectSystemsToAddToGroupView)
        else:
            systemGroupView = SystemGroupView(self.systemGroup)
            await interaction.response.edit_message(embed=systemGroupView.getEmbed(),view=systemGroupView)


    @discord.ui.button(label="Delete System Group", style=discord.ButtonStyle.danger, row=2)
    async def deleteSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        deleteSystemGroupConfirmationModal = DeleteSystemGroupConfirmationModal(self.systemGroup.name)
        await interaction.response.send_modal(deleteSystemGroupConfirmationModal)
        await deleteSystemGroupConfirmationModal.wait()


    def getEmbed(self):
        description="Systems:"
        for systemName in self.systemGroup.systems:
                description += f"\n{systemName}"

        title = ""
        if self.systemGroup.emote!=None:
            title = f"Edit System Group: {self.systemGroup.emote} {self.systemGroup.name} {self.systemGroup.emote}"
        else:
            title = f"Edit System Group: {self.systemGroup.name}"
        embed = discord.Embed(
            title=title,
            description=description
        )
        return embed

import discord

#custom
from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup
from Discord.View.SystemGroup.Edit.SystemGroupDeletedView import SystemGroupDeletedView
from Discord.Modal.SystemGroup.Edit.DeleteSystemGroupConfirmationModal import DeleteSystemGroupConfirmationModal

class EditSystemGroupView(discord.ui.View):
    def __init__(self, systemGroupName: str):
        super().__init__()
        self.systemGroup = systemGroupName

    @discord.ui.button(label="Delete System Group", style=discord.ButtonStyle.danger)
    async def deleteSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        deleteSystemGroupConfirmationModal = DeleteSystemGroupConfirmationModal(self.systemGroup)
        await interaction.response.send_modal(deleteSystemGroupConfirmationModal)
        await deleteSystemGroupConfirmationModal.wait()

        if deleteSystemGroupConfirmationModal.systemGroupNameInput.value == self.systemGroup:
            DataManager.removeSystemGroup(interaction.guild_id,self.systemGroup)
            systemGroupDeletedView = SystemGroupDeletedView(self.systemGroup)
            await interaction.message.edit(embed=systemGroupDeletedView.getEmbed(),view=systemGroupDeletedView)
        else:
            await interaction.message.edit(embed=self.getEmbed(),view=self)

    def getEmbed(self):
        embed = discord.Embed(
            title=f"Edit System Group: {self.systemGroup}",
            description="TBA: System List"
        )
        return embed

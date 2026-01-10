import discord

from DataManager import DataManager

class DeleteSystemGroupConfirmationModal(discord.ui.Modal):
    def __init__(self, systemGroupName: str):
        super().__init__(title=f"Delete System Group: {systemGroupName}")
        self.systemGroupName = systemGroupName

        self.systemGroupNameInput = discord.ui.InputText(
            label="Enter System Group Name to confirm",
            placeholder=self.systemGroupName,
            required=True
            )
        self.add_item(self.systemGroupNameInput)

    async def callback(self, interaction: discord.Interaction):
        textInput = self.systemGroupNameInput.value

        if textInput.lower() == self.systemGroupName.lower():
            removed = DataManager.removeSystemGroup(interaction.guild_id,self.systemGroupName)
            if removed:
                await interaction.response.send_message(f"\"{self.systemGroupName.title()}\" System Group Succesfully Deleted!",ephemeral=True)
            else:
                await interaction.response.send_message(f"Error, can't delete \"{self.systemGroupName.title()}\" System Group.",ephemeral=True)

            #trouver une solution plus propre
            from Discord.View.SystemGroup.SystemGroupsView import SystemGroupsView
            systemGroupsView = SystemGroupsView(DataManager.getSystemGroups(interaction.guild_id))
            await interaction.message.edit(embed=systemGroupsView.getEmbed(), view=systemGroupsView)
        else:
            await interaction.response.send_message("Cases do not match, deletion canceled.",ephemeral=True)
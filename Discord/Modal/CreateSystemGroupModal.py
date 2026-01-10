import discord

from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup
from Discord.View.SystemGroup.Edit.SystemGroupView import SystemGroupView

class CreateSystemGroupModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create System Group")

        self.systemGroupName = discord.ui.InputText(label="Group Name")
        self.add_item(self.systemGroupName)

    async def callback(self, interaction: discord.Interaction):
        groupName = str(self.systemGroupName.value)
        systemGroup = DataManager.getSystemGroup(interaction.guild_id, groupName)
        if systemGroup == None:
            systemGroup = SystemGroup(name=groupName)
            DataManager.saveSystemGroup(interaction.guild_id, systemGroup)

            await interaction.response.send_message(f"System Group \"{self.systemGroupName.value}\" created!", ephemeral=True)
        else:
            await interaction.response.send_message(f"System Group \"{self.systemGroupName.value}\" already exist.", ephemeral=True)
        
        systemGroupView = SystemGroupView(systemGroup)
        await interaction.edit_original_response(embed=systemGroupView.getEmbed(), view=systemGroupView)

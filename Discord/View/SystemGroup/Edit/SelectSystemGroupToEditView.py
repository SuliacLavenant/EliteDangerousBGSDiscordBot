import discord

#custom
from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup
from Discord.View.SystemGroup.SelectSystemGroupView import SelectSystemGroupView
from Discord.View.SystemGroup.Edit.EditSystemGroupView import EditSystemGroupView

class SelectSystemGroupToEditView(SelectSystemGroupView):
    action: str = "Edit"

    async def selectSystemGroup_callback(self, interaction: discord.Interaction):
        selected = self.select.values[0]
        editSystemGroupView = EditSystemGroupView(DataManager.getSystemGroup(interaction.guild_id,selected))
        await interaction.response.edit_message(embed=editSystemGroupView.getEmbed(),view=editSystemGroupView)
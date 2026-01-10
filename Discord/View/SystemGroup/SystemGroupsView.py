import discord

#custom
from BotConfig.BotConfig import BotConfig
from DataManager import DataManager
from Discord.Modal.CreateSystemGroupModal import CreateSystemGroupModal
from Discord.View.SystemGroup.Edit.SystemGroupView import SystemGroupView

from DataClass.SystemGroup import SystemGroup

class SystemGroupsView(discord.ui.View):
    def __init__(self, systemGroups):
        super().__init__()
        self.systemGroups = systemGroups

        selectOptions = []
        for systemGroup in self.systemGroups:
            selectOption = discord.SelectOption(label=systemGroup.name)
            selectOptions.append(selectOption)
        
        self.select = discord.ui.Select(
            placeholder = f"Select a System Group",
            min_values = 1,
            max_values = 1,
            options = selectOptions
        )
        self.select.callback = self.selectSystemGroup_callback
        self.add_item(self.select)


    @discord.ui.button(label="Create New Group", style=discord.ButtonStyle.success)
    async def CreateNewGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        createSystemGroupModal = CreateSystemGroupModal()
        await interaction.response.send_modal(createSystemGroupModal)
        await createSystemGroupModal.wait()


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


    async def selectSystemGroup_callback(self, interaction: discord.Interaction):
        selected = self.select.values[0]
        systemGroupView = SystemGroupView(DataManager.getSystemGroup(interaction.guild_id,selected))
        await interaction.response.edit_message(embed=systemGroupView.getEmbed(),view=systemGroupView)

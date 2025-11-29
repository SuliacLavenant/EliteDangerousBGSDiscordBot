import discord
from math import ceil

#custom
from DataManager import DataManager
from DataClass.SystemGroup import SystemGroup

class SelectSystemsToAddToGroupView(discord.ui.View):
    action: str = ""

    def __init__(self, systemGroup: SystemGroup, systemNames: str, page: tuple = None):
        super().__init__()
        self.systemGroup = systemGroup
        self.systemNames = systemNames
        self.page = page

        self.needMoreSelect = len(self.systemNames)>25
        if self.page!=None:
            self.page = (self.page[0]+1,self.page[1])
        if self.needMoreSelect and self.page == None:
            self.page = (1,ceil(len(self.systemNames)/25))

        systemsInSelect = self.systemNames[:24]
        selectOptions = []
        for systemName in systemsInSelect:
            selectOption = discord.SelectOption(label=systemName)
            selectOptions.append(selectOption)
        
        self.select = discord.ui.Select(
            placeholder = f"Select Systems to add to Group",
            min_values = 0,
            max_values = len(systemsInSelect),
            options = selectOptions
        )
        self.select.callback = self.selectSystems_callback
        self.add_item(self.select)

    @discord.ui.button(label="next", style=discord.ButtonStyle.primary)
    async def addSystemsToSystemGroup(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.needMoreSelect:
            selectSystemsToAddToGroupView = SelectSystemsToAddToGroupView(self.systemGroup, self.systemNames[24:],self.page)
            await interaction.response.edit_message(embed=selectSystemsToAddToGroupView.getEmbed(),view=selectSystemsToAddToGroupView)

        else:
            DataManager.saveSystemGroup(interaction.guild_id,self.systemGroup)
            await interaction.response.send_message(f"systems added", ephemeral=True)

    def getEmbed(self):
        title = f"Select Systems to add to Group"
        if self.page!=None:
            title = f"Select Systems to add to Group page {self.page[0]}/{self.page[1]}"
        embed = discord.Embed(title=title)
        return embed

    async def selectSystems_callback(self, interaction: discord.Interaction):
        for systemName in self.select.values:
            self.systemGroup.addSystem(systemName)

        if self.needMoreSelect:
            selectSystemsToAddToGroupView = SelectSystemsToAddToGroupView(self.systemGroup, self.systemNames[24:],self.page)
            await interaction.response.edit_message(embed=selectSystemsToAddToGroupView.getEmbed(),view=selectSystemsToAddToGroupView)

        else:
            DataManager.saveSystemGroup(interaction.guild_id,self.systemGroup)
            await interaction.response.send_message(f"systems added", ephemeral=True)

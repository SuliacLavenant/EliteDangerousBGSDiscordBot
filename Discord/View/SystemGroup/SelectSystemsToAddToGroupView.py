import discord
from math import ceil

#custom
from DataClass.SystemGroup import SystemGroup
from DataStorageManager import DataStorageManager

class SelectSystemsToAddToGroupView(discord.ui.View):
    system_group: SystemGroup
    system_names: list
    page: tuple


    def __init__(self, system_group: SystemGroup, system_names: list, page: tuple = None):
        super().__init__()
        self.system_group = system_group
        self.system_names = system_names
        self.page = page

        if self.page!=None:
            self.page = (self.page[0]+1,self.page[1])
        elif self.need_more_select() and self.page == None:
            self.page = (1,ceil(len(self.system_names)/25))

        systems_in_select = self.system_names[:24]
        select_options = []
        for system_name in systems_in_select:
            select_option = discord.SelectOption(label=system_name)
            select_options.append(select_option)
        
        self.select = discord.ui.Select(
            placeholder = f"Select System(s) to add to Group:",
            min_values = 0,
            max_values = len(systems_in_select),
            options = select_options
        )
        self.select.callback = self.select_systems_callback
        self.add_item(self.select)


    @discord.ui.button(label="next", style=discord.ButtonStyle.primary)
    async def next_systems(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.process_select_systems(interaction)


    async def select_systems_callback(self, interaction: discord.Interaction):
        for systemName in self.select.values:
            self.system_group.addSystem(systemName)
        await self.process_select_systems(interaction)


    async def process_select_systems(self, interaction: discord.Interaction):
        if self.need_more_select():
            select_systems_to_add_to_group_view = SelectSystemsToAddToGroupView(self.system_group, self.system_names[24:],self.page)
            await interaction.response.edit_message(embed=select_systems_to_add_to_group_view.get_embed(),view=select_systems_to_add_to_group_view)

        else:
            DataStorageManager.storeSystemGroup(interaction.guild_id,self.system_group)
            self.system_group = DataStorageManager.getSystemGroup(interaction.guild_id,self.system_group.name)

            from Discord.View.SystemGroup.SystemGroupView import SystemGroupView
            system_group_view = SystemGroupView(self.system_group)
            await interaction.response.edit_message(embed=system_group_view.get_embed(),view=system_group_view)


    def get_embed(self):
        title = f"Select Systems to add to Group"
        if self.page!=None:
            title += f" {self.page[0]}/{self.page[1]}"
        embed = discord.Embed(title=title)
        return embed


    def need_more_select(self):
        return len(self.system_names)>25

import discord

class SelectSystemsToAddToSystemGroupModal(discord.ui.DesignerModal):
    system_name_list: list
    system_name_to_add_list: list

    systems_selects: list

    def __init__(self, system_name_list: list):
        super().__init__(title="Select Systems To Add To System Group")
        
        self.system_name_list = system_name_list
        self.system_name_list.sort()
        
        self.systems_selects = []
        options = []
        for system_name in self.system_name_list:
            options.append(discord.SelectOption(label=system_name, value=system_name))
            if len(options)>=20:
                systems_select = discord.ui.Label(label="Systems:").set_select(
                    options=options,
                    min_values=0,
                    max_values=len(options),
                    default_values=None,
                    required=False
                )
                self.add_item(systems_select)
                self.systems_selects.append(systems_select)
                options = []

        if len(options)>=1:
            systems_select = discord.ui.Label(label="Systems:").set_select(
                options=options,
                min_values=0,
                max_values=len(options),
                default_values=None,
                required=False
            )
            self.add_item(systems_select)
            self.systems_selects.append(systems_select)


    async def callback(self, interaction: discord.Interaction):
        self.system_name_to_add_list= []
        for systems_select in self.systems_selects:
            for system_name in systems_select.item.values:
                self.system_name_to_add_list.append(system_name)

        await interaction.response.defer()

import discord

from DataClass.DiscordTrackedSystem import DiscordTrackedSystem 


class SelectSystemsToRemoveFromSystemGroupModal(discord.ui.DesignerModal):
    tracked_systems: list
    system_names_to_remove: list

    systems_selects: list

    def __init__(self, tracked_systems: list):
        super().__init__(title="Select Systems To Remove From System Group")
        
        self.tracked_systems = tracked_systems
        # self.tracked_systems.sort()
        
        self.systems_selects = []
        options = []
        for tracked_system in self.tracked_systems:
            options.append(discord.SelectOption(label=tracked_system.system.name, value=tracked_system.system.name))
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
        await interaction.response.defer()
        self.system_names_to_remove= []
        for systems_select in self.systems_selects:
            for system_name in systems_select.item.values:
                self.system_names_to_remove.append(system_name)

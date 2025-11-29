import discord

#custom
from DataClass.SystemGroup import SystemGroup

class SelectSystemGroupView(discord.ui.View):
    action: str = ""

    def __init__(self, systemGroups: list):
        super().__init__()
        self.systemGroups = systemGroups

        selectOptions = []
        for systemGroup in self.systemGroups:
            selectOption = discord.SelectOption(label=systemGroup.name)
            selectOptions.append(selectOption)
        
        self.select = discord.ui.Select(
            placeholder = f"Select a System Group to {self.action}",
            min_values = 1,
            max_values = 1,
            options = selectOptions
        )
        self.select.callback = self.selectSystemGroup_callback
        self.add_item(self.select)

    def getEmbed(self):
        title = f"Select System Group to {self.action}"
        embed = discord.Embed(title=title)

        return embed

    async def selectSystemGroup_callback(self, interaction: discord.Interaction):
        selected = self.select.values[0]
        await interaction.response.send_message(f"Selected: **{selected}**", ephemeral=True)
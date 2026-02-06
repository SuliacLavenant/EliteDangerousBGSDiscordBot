import discord

class SetColorForSystemGroupModal(discord.ui.DesignerModal):
    manual_entry: bool = False
    color: discord.Color = None

    def __init__(self):
        super().__init__(title="Set Color For System Group")

        self.color_select = discord.ui.Label(label="Color:").set_select(
            options=[
                discord.SelectOption(label="Black", value="black", emoji="⬛"),
                discord.SelectOption(label="Blue", value="blue", emoji="🟦"),
                discord.SelectOption(label="Green", value="green", emoji="🟩"),
                discord.SelectOption(label="Orange", value="orange", emoji="🟧"),
                discord.SelectOption(label="Pink", value="fuchsia", emoji="🩷"),
                discord.SelectOption(label="Purple", value="purple", emoji="🟪"),
                discord.SelectOption(label="Red", value="red", emoji="🟥"),
                discord.SelectOption(label="Teal", value="teal", emoji="🩵"),
                discord.SelectOption(label="White", value="white", emoji="🤍"),
                discord.SelectOption(label="Yellow", value="yellow", emoji="🟨"),
            ],
            min_values=1,
            max_values=1,
            default_values=None
        )

        self.add_item(self.color_select)


    async def callback(self, interaction: discord.Interaction):
        color_txt = self.color_select.item.values[0]
        #if color_txt != None:
        
        match self.color_select.item.values[0]:
            case "black":
                self.color = discord.Color.from_rgb(0,0,0)
            case "blue":
                self.color = discord.Color.blue()
            case "fuchsia":
                self.color = discord.Color.fuchsia()
            case "green":
                self.color = discord.Color.green()
            case "orange":
                self.color = discord.Color.orange()
            case "purple":
                self.color = discord.Color.purple()
            case "red":
                self.color = discord.Color.red()
            case "teal":
                self.color = discord.Color.teal()
            case "white":
                self.color = discord.Color.from_rgb(255,255,255)
            case "yellow":
                self.color = discord.Color.yellow()
            case _:
                self.color = None

        await interaction.response.defer()

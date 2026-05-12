import discord

from DataClass.Player import Player

class SetSystemArchitectModal(discord.ui.DesignerModal):
    player_id: int = None
    player_list: list[Player]
    players_selects: list

    def __init__(self, player_list: list):
        super().__init__(title=f"Set System Architect")
        self.player_list = player_list
        #self.player_name_list.sort()
        
        self.players_selects = []
        options = []
        for player in self.player_list:
            options.append(discord.SelectOption(label=player.name, value=str(player.id)))
            if len(options)>=20:
                players_select = discord.ui.Label(label="Player:").set_select(
                    options=options,
                    min_values=0,
                    max_values=1,
                    default_values=None,
                    required=False
                )
                self.add_item(players_select)
                self.players_selects.append(players_select)
                options = []

        if len(options)>=1:
            players_select = discord.ui.Label(label="Player:").set_select(
                options=options,
                min_values=0,
                max_values=1,
                default_values=None,
                required=False
            )
            self.add_item(players_select)
            self.players_selects.append(players_select)


    async def callback(self, interaction: discord.Interaction):
        for players_select in self.players_selects:
            self.player_id = int(players_select.item.values[0])

        await interaction.response.defer()

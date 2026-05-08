import discord

from DataClass.Player import Player

class AddPlayerToSquadronModal(discord.ui.DesignerModal):
    player_list: list
    player_id_to_add_list: list

    players_selects: list

    def __init__(self, player_list: list):
        super().__init__(title=f"Select Players To Add To Squadron")
        
        self.player_list = player_list
        #self.player_name_list.sort()
        
        self.players_selects = []
        options = []
        for player in self.player_list:
            options.append(discord.SelectOption(label=player.name, value=str(player.id)))
            if len(options)>=20:
                players_select = discord.ui.Label(label="Players:").set_select(
                    options=options,
                    min_values=0,
                    max_values=len(options),
                    default_values=None,
                    required=False
                )
                self.add_item(players_select)
                self.players_selects.append(players_select)
                options = []

        if len(options)>=1:
            players_select = discord.ui.Label(label="Players:").set_select(
                options=options,
                min_values=0,
                max_values=len(options),
                default_values=None,
                required=False
            )
            self.add_item(players_select)
            self.players_selects.append(players_select)


    async def callback(self, interaction: discord.Interaction):
        self.player_id_to_add_list = []
        for players_select in self.players_selects:
            for player_id in players_select.item.values:
                self.player_id_to_add_list.append(int(player_id))

        await interaction.response.defer()

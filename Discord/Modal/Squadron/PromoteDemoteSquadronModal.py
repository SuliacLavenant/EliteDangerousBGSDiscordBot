import discord

from DataClass.Player import Player

class PromoteDemoteSquadronModal(discord.ui.DesignerModal):
    player_list: list
    player_id_to_promote_demote: list
    player_ranks: list
    player_rank: str

    players_selects: list
    rank_select: discord.ui.Label

    def __init__(self, player_list: list, player_ranks: list):
        super().__init__(title=f"Select Players To Remove Fromm Squadron")
        
        self.player_list = player_list
        self.player_ranks = player_ranks
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

        options = []
        for player_rank in self.player_ranks:
            options.append(discord.SelectOption(label=player_rank, value=player_rank))
        self.rank_select = discord.ui.Label(label="Rank To Promote/Demote to:").set_select(
            options=options,
            min_values=1,
            max_values=1,
            default_values=None,
            required=True
        )
        self.add_item(self.rank_select)


    async def callback(self, interaction: discord.Interaction):
        self.player_id_to_promote_demote = []
        for players_select in self.players_selects:
            for player_id in players_select.item.values:
                self.player_id_to_promote_demote.append(int(player_id))

        self.player_rank = self.rank_select.item.values[0]

        await interaction.response.defer()

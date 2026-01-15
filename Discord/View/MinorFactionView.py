import discord
import urllib.parse

#custom
from DataManager import DataManager

from DataClass.MinorFaction import MinorFaction

from Discord.Modal.SetMinorFactionModal import SetMinorFactionModal

class MinorFactionView(discord.ui.View):
    def __init__(self, minorFaction: MinorFaction):
        super().__init__()
        self.minorFaction = minorFaction

        if self.minorFaction != None:
            self.remove_item(self.setMinorFaction)
            self.add_item(discord.ui.Button(
                label="Inara",
                url=f"https://inara.cz/elite/minorfaction/?search={urllib.parse.quote(self.minorFaction.name)}",
                emoji="🌐"
            ))


    @discord.ui.button(label="Set Minor Faction", style=discord.ButtonStyle.primary)
    async def setMinorFaction(self, button: discord.ui.Button, interaction: discord.Interaction):
        setMinorFactionModal = SetMinorFactionModal()
        await interaction.response.send_modal(setMinorFactionModal)
        await setMinorFactionModal.wait()
        minorFactionName = setMinorFactionModal.minorFactionName.value
        if DataManager.setPlayerMinorFaction(interaction.guild_id,minorFactionName):
            await interaction.followup.send(f"Minor Faction \"{minorFactionName.lower().title()}\" Successfully set!", ephemeral=True)
            minorFaction = DataManager.getMinorFaction(interaction.guild_id)
            minorFactionView = MinorFactionView(minorFaction)
            await interaction.edit_original_response(view=minorFactionView,embed=minorFactionView.getEmbed())
        else:
            await interaction.followup.send(f"cannot find \"{minorFactionName.lower().title()}\" Minor Faction. This can happen if the faction does not exist, if it is a recent addition, or if the API has not responded.")



    def getEmbed(self):
        if self.minorFaction == None:
            return self.getNoMinorFactionEmbed()
        else:
            return self.getFactionRecapEmbed()


    def getNoMinorFactionEmbed(self):
        embed = discord.Embed(
            title="No Minor Faction Set",
            description="Please set a Minor Faction"
        )
        return embed


    def getFactionRecapEmbed(self):
        title = self.minorFaction.name.title()
        description = f"Allegiance: **{self.minorFaction.allegiance.title()}**\n"
        description += f"Government: **{self.minorFaction.government.title()}**\n"
        description += f"Origin System: [**{self.minorFaction.originSystemName.title()}**](https://inara.cz/elite/starsystem/?search={urllib.parse.quote(self.minorFaction.originSystemName)})"
        
        embed = discord.Embed(title=title, description=description)

        embed.add_field(name=f"Systems", value=f"Present in **{self.minorFaction.numberOfSystems}** systems. \n Controlling **TBA** systems.", inline=True)

        return embed

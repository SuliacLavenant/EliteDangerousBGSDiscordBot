import discord

class CreateSystemGroupModal(discord.ui.Modal, title="Create System Group"):
    groupName = discord.ui.TextInput(label="Group Name")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.groupName, ephemeral=True)
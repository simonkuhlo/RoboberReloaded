import discord
from ..views import select_event
from ...ref import event

class Button(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.label = "Edit Event"
        self.style = discord.ButtonStyle.blurple
        self.event = event

    async def callback(self, interaction:discord.Interaction):
        options = await select_event.get_editable_events(interaction.guild, interaction.user)
        if options:
            await interaction.response.send_message(f"Select the event you want to edit:", ephemeral=True, view = select_event.View(options))
        else:
            await interaction.response.send_message("No editable events found for this user.", ephemeral=True)
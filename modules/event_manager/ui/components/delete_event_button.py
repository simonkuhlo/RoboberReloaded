import discord
from ...ref import event
from ... import api

class Button(discord.ui.Button):
    def __init__(self, event:event.Event):
        super().__init__()
        self.label = "Delete Event"
        self.style = discord.ButtonStyle.red
        self.event = event

    async def callback(self, interaction:discord.Interaction):
        await api.delete_event(self.event)
        await interaction.response.send_message(f"Event {self.event.name} deleted!", ephemeral=True)
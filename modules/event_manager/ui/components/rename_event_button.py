import discord
from ...ref import event as event_ref
from ... import api

class RenameModal(discord.ui.Modal):
    def __init__(self, event:event_ref.Event):
        title="Rename event"
        super().__init__(title=title, timeout=None, custom_id="EventRenameModal")
        self.event:event_ref.Event = event

    name = discord.ui.TextInput(
        label="New name",
        placeholder="Enter the new event name..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        await api.rename_event(self.event, self.name.value)
        await interaction.response.send_message(f"Event {self.event.name} updated.", ephemeral=True)

class Button(discord.ui.Button):
    def __init__(self, event:event_ref.Event):
        super().__init__()
        self.label = "Rename Event"
        self.style = discord.ButtonStyle.blurple
        self.event = event

    async def callback(self, interaction:discord.Interaction):
        await interaction.response.send_modal(RenameModal(self.event))
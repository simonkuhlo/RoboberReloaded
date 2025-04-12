import discord
from ...components import delete_event_button, rename_event_button
from ....ref import event

class View(discord.ui.View):
    def __init__(self, event:event.Event):
        super().__init__(timeout=600)
        # addd buttons
        self.add_item(rename_event_button.Button(event))
        self.add_item(delete_event_button.Button(event))
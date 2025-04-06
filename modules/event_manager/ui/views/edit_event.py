import discord
from ..items import delete_event, rename_event
from ...ref import event

class View(discord.ui.View):
    def __init__(self, event:event.Event):
        super().__init__(timeout=600)
        # addd buttons
        self.add_item(rename_event.Button(event))
        self.add_item(delete_event.Button(event))
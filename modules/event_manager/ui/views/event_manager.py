import discord
from ..items import edit_start


class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        # addd buttons
        self.add_item(edit_start.Button())
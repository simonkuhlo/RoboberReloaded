import discord
from ...components import edit_start_button


class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # addd buttons
        self.add_item(edit_start_button.Button())
import discord
from ..views.edit import edit_menu
from ...ref import event as event_ref


class Select(discord.ui.Select):
    def __init__(self, options:list[discord.SelectOption]):
        options = options
        super().__init__(placeholder="Choose an option...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction:discord.Interaction):
        event = await event_ref.from_db_with_id(self.values[0])
        await interaction.response.edit_message(content=f"You selected {event.name}", view=edit_menu.View(event))
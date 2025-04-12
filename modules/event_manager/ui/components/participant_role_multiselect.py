import discord
from ..views.edit import edit_menu
from ...ref import event as event_ref


class Select(discord.ui.Select):
    def __init__(self, options:list[discord.SelectOption]):
        super().__init__(placeholder="Choose an option...", options=options, min_values=1, max_values=len(options))

    async def callback(self, interaction:discord.Interaction):
        for value in self.values:
            event = await event_ref.from_db_with_id(value)
            await interaction.user.add_roles(event.participant_role)
        await interaction.response.edit_message(content=f"Roles should have been added")                                               
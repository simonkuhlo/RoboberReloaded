import discord
from ...ref import event as event_ref
from ..components import participant_role_multiselect

async def get_selectable_events(guild:discord.Guild, member:discord.Member) -> list[discord.SelectOption]:
    all_events = await event_ref.all_from_guild(guild.id)
    editable_events = []
    for event in all_events:
        select_option = discord.SelectOption(label=event.name, value=str(event.id))
        editable_events.append(select_option)
    return editable_events

class View(discord.ui.View):
    def __init__(self, options:list[discord.SelectOption]):
        super().__init__(timeout=None)
        # addd buttons
        self.add_item(participant_role_multiselect.Select(options))
import discord
from ..components import edit_event_selector
from ...ref import event as event_ref


async def get_editable_events(guild:discord.Guild, member:discord.Member) -> list[event_ref.Event]:
    all_events = await event_ref.all_from_guild(guild.id)
    print(all_events)
    editable_events = []
    for event in all_events:
        if event.administrator_role in member.roles:
            select_option = discord.SelectOption(label=event.name, value=str(event.id))
            editable_events.append(select_option)
    return editable_events

class View(discord.ui.View):
    def __init__(self, options:list[discord.SelectOption]):
        super().__init__(timeout=600)
        # addd buttons
        self.add_item(edit_event_selector.Select(options))
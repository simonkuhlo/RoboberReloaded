import copy
import discord
from . import event_manager_discord_helper
from core_app import db_model as db

class EditButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Events bearbeiten", style=discord.ButtonStyle.primary, emoji="🔧")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        editable_events = await get_editable_events(interaction.guild, interaction.user)
        if editable_events:
            view = await select_view_factory(editable_events=editable_events)
            await interaction.response.send_message(f"Du hast {len(editable_events)} Events, die du bearbeiten kannst. Wähle das Event, das du bearbeiten möchtest: ", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("No editable events found for this user.", ephemeral=True)

async def get_editable_events(guild:discord.Guild, member:discord.Member) -> list[db.EventDiscordWrapper]:
    db_instance:db.GuildDB = db.get_db_instance(guild=guild)
    all_events:list[db.EventDiscordWrapper] = await db_instance.get_all_events()
    editable_events = []
    for event in all_events:
        if event.administrator_role in member.roles or 1 == 1:
            select_option = discord.SelectOption(label=event.name, value=str(event.db_id))
            editable_events.append(select_option)
    return editable_events


class EventEditView(discord.ui.View):
    def __init__(self, event:db.EventDiscordWrapper):
        super().__init__(timeout=600)
        # addd buttons
        self.add_item(RenameEventButton(event))
        self.add_item(DeleteEventButton(event))


class EventSelector(discord.ui.Select):
    def __init__(self, options:list[discord.SelectOption]):
        options = options
        super().__init__(placeholder="Choose an option...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction:discord.Interaction):
        db_instance = db.get_db_instance(interaction.guild)
        event = await db_instance.get_event(self.values[0])
        edit_view = EventEditView(event)
        await interaction.response.edit_message(content=f"You selected {event.name}", view=edit_view)
        

class EventSelectView(discord.ui.View):
    def __init__(self, selector:EventSelector):
        super().__init__(timeout=600)
        self.add_item(selector)

async def select_view_factory(editable_events:list[db.EventDiscordWrapper]):
    selector = EventSelector(options=editable_events)
    view = EventSelectView(selector=selector)
    return view



class DeleteEventButton(discord.ui.Button):
    def __init__(self, event:db.EventDiscordWrapper):
        super().__init__()
        self.label = "Delete Event"
        self.style = discord.ButtonStyle.red
        self.event:db.EventDiscordWrapper = event

    async def callback(self, interaction:discord.Interaction):
        await event_manager_discord_helper.delete_event(guild=interaction.guild, event=self.event)
        await interaction.response.send_message(f"Event {self.event.name} deleted.", ephemeral=True)

class RenameEventButton(discord.ui.Button):
    def __init__(self, event:db.EventDiscordWrapper):
        super().__init__()
        self.label = "Rename Event"
        self.style = discord.ButtonStyle.blurple
        self.event:db.EventDiscordWrapper = event

    async def callback(self, interaction:discord.Interaction):
        new_event = copy.copy(self.event)
        new_event.name = "Daniels 2ter Geburtstag"
        updated_event = db.EventDiscordWrapperUpdate(self.event, new_event)
        await event_manager_discord_helper.edit_event(interaction.guild, updated_event)
        await interaction.response.send_message(f"Event {self.event.name} updated.", ephemeral=True)



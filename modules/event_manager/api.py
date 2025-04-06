import discord
from . import ref
from . import discord_worker

async def create_event(guild:discord.Guild, name:str):
    event = ref.event.Event(guild, name)
    await discord_worker.create_event(event)
    event.save()

async def rename_event(event:ref.event.Event, new_name:str):
    event.rename(new_name)
    await discord_worker.rename_event(event)

async def delete_event(event:ref.event.Event):
    await discord_worker.delete_event(event)
    event.delete()
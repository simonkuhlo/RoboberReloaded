# handles interaction with discord
import discord
from .ref import event

async def create_event(event:event.Event):
    if not event.participant_role:
        event.participant_role = await event.guild.create_role(name=f"{event.name}-Teilnehmer")
    
    if not event.administrator_role:
        event.administrator_role = await event.guild.create_role(name=f"{event.name}-Administrator")

    if not event.category:
        event.category = await event.guild.create_category(event.name, overwrites={event.guild.default_role: discord.PermissionOverwrite(view_channel=False)})
        await event.guild.create_text_channel(
        name = "info", 
        category = event.category,
        overwrites={
            event.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.participant_role: discord.PermissionOverwrite(view_channel=True, send_messages=False),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })
        await event.guild.create_text_channel(
        name = "planung", 
        category = event.category,
        overwrites={
            event.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })
        await event.guild.create_text_channel(
        name = "chat", 
        category = event.category,
        overwrites={
            event.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.participant_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })

async def rename_event(event:event.Event):
    await event.category.edit(name=event.name)
    await event.participant_role.edit(name=f"{event.name}-Teilnehmer")
    await event.administrator_role.edit(name=f"{event.name}-Administrator")

async def delete_event(event:event.Event):                                                     
    if event.category:
        for channel in event.category.channels:
            await channel.delete()
        await event.category.delete()
    if event.participant_role:
        await event.participant_role.delete()
    if event.administrator_role:
        await event.administrator_role.delete()
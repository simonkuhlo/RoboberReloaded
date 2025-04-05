import core_app.db_model as db
import discord

async def create_event(guild:discord.Guild, event:db.EventDiscordWrapper):
    if not event.participant_role:
        event.participant_role = await guild.create_role(name=f"{event.name}-Teilnehmer")
    
    if not event.administrator_role:
        event.administrator_role = await guild.create_role(name=f"{event.name}-Administrator")

    if not event.category:
        event.category = await guild.create_category(event.name, overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False)})
        await guild.create_text_channel(
        name = "info", 
        category = event.category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.participant_role: discord.PermissionOverwrite(view_channel=True, send_messages=False),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })
        await guild.create_text_channel(
        name = "planung", 
        category = event.category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })
        await guild.create_text_channel(
        name = "chat", 
        category = event.category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            event.participant_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            event.administrator_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        })
    db.get_db_instance(guild).save_event(event=event)

async def edit_event(guild:discord.Guild, updated_event:db.EventDiscordWrapperUpdate):
    if updated_event.old.name != updated_event.new.name:
        await updated_event.new.category.edit(name=updated_event.new.name)
        await updated_event.new.participant_role.edit(name=f"{updated_event.new.name}-Teilnehmer")
        await updated_event.new.administrator_role.edit(name=f"{updated_event.new.name}-Administrator")
    db.get_db_instance(guild).change_event(updated_event=updated_event)

async def delete_event(guild:discord.Guild, event:db.EventDiscordWrapper):                                                     
    if event.category:
        for channel in event.category.channels:
            await channel.delete()
        await event.category.delete()
    if event.participant_role:
        await event.participant_role.delete()
    if event.administrator_role:
        await event.administrator_role.delete()
    db.get_db_instance(guild).delete_event(event=event)



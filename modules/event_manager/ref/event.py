import discord
from ..db import db_worker
from .. import ref

from discord.ext import commands


class Event():
    def __init__(
                self, 
                guild:discord.Guild, 
                name:str, 
                category:discord.CategoryChannel=None, 
                participant_role:discord.Role=None, 
                administrator_role:discord.Role=None, 
                db_id:int=None
                ):
        self.guild:discord.Guild = guild
        self.id:int = db_id
        self.name:str = name
        self.category:discord.CategoryChannel = category
        self.participant_role:discord.Role = participant_role
        self.administrator_role:discord.Role = administrator_role
    
    def save(self):
        with db_worker.orm.db_session:
            if self.id:
                db_object = db_worker.Event[self.id]
                db_object.guild_id = str(self.guild.id)
                db_object.name = self.name
                db_object.category_id = str(self.category.id)
                db_object.administrator_role_id = str(self.administrator_role.id)
                db_object.participant_role_id = str(self.participant_role.id)
            else:
                db_worker.Event(
                    guild_id = str(self.guild.id),
                    name = self.name,
                    category_id = str(self.category.id),
                    administrator_role_id = str(self.administrator_role.id),
                    participant_role_id = str(self.participant_role.id)
                )

    def rename(self, new_name:str):
        self.name = new_name
        self.save()

    def delete(self):
        if self.id:
            with db_worker.orm.db_session:
                db_worker.Event[self.id].delete()

async def from_db_with_id(id:int):
    with db_worker.orm.db_session:
        return(await from_db(db_worker.Event[id]))

async def from_db(db_object:db_worker.Event) -> Event:
    with db_worker.orm.db_session:
        guild:discord.Guild = ref.bot.get_guild(int(db_object.guild_id))
        event_category:discord.CategoryChannel = None
        participant_role:discord.Role = guild.get_role(int(db_object.participant_role_id))
        administrator_role:discord.Role = guild.get_role(int(db_object.administrator_role_id))
        for category in guild.categories:
            if int(category.id) == int(db_object.category_id):
                event_category = category
                break
        
        event_object = Event(
            guild = guild,
            db_id = db_object.id,
            name = db_object.name,
            category = event_category,
            participant_role = participant_role,
            administrator_role = administrator_role
        )
    return event_object

async def all_from_guild(guild_id:int) -> list[Event]:
    guild_events:list[Event] = []
    with db_worker.orm.db_session:
        db_obects = db_worker.Event.select()
        for db_object in db_obects:
            event = await from_db(db_object)
            guild_events.append(event)
    return guild_events
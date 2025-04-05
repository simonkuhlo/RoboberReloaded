from pony import orm
import discord

db_instances:dict = {

}

class EventDiscordWrapper():
    def __init__(self, name:str, category:discord.CategoryChannel=None, participant_role:discord.Role=None, administrator_role:discord.Role=None, db_id:int=None):
        self.db_id:int = db_id
        self.name:str = name
        self.category:discord.CategoryChannel = category
        self.participant_role:discord.Role = participant_role
        self.administrator_role:discord.Role = administrator_role

class EventDiscordWrapperUpdate():
    def __init__(self, old:EventDiscordWrapper, new:EventDiscordWrapper):
        self.old = old
        self.new = new

class GuildDB():
    def __init__(self, guild:discord.Guild):
        self.guild:discord.Guild = guild
        self.db = orm.Database()
        self.db.bind(provider='sqlite', filename=f'{self.guild.id}.sqlite', create_db=True)
        self._define_entities()
        self.db.generate_mapping(create_tables=True)
        db_instances[self.guild.id] = self
    
    def _define_entities(self):
        class EventDBWrapper(self.db.Entity):
            name = orm.Required(str)
            category_id = orm.Required(str)
            participant_role_id = orm.Required(str)
            administrator_role_id = orm.Required(str)
        self.EventDBWrapper = EventDBWrapper
        
    
    

    async def discord_wrapper_from_db(self, db_object_id:str) -> EventDiscordWrapper:
        event_category:discord.CategoryChannel = None
        participant_role:discord.Role = None
        administrator_role:discord.Role = None
        with orm.db_session:
            db_object = self.EventDBWrapper[db_object_id]
            participant_role = self.guild.get_role(int(db_object.participant_role_id))
            administrator_role = self.guild.get_role(int(db_object.administrator_role_id))
            for category in self.guild.categories:
                if int(category.id) == int(db_object.category_id):
                    event_category = category
                    break
        discord_wrapper_object = EventDiscordWrapper(
            db_id = db_object.id,
            name = db_object.name,
            category = event_category,
            participant_role = participant_role,
            administrator_role = administrator_role
        )
        return discord_wrapper_object

    

    @orm.db_session
    def save_event(self, event:EventDiscordWrapper):
        self.EventDBWrapper(
            name = event.name,
            category_id = str(event.category.id),
            participant_role_id = str(event.participant_role.id),
            administrator_role_id = str(event.administrator_role.id)
        )

    @orm.db_session
    def change_event(self, updated_event:EventDiscordWrapperUpdate):
        db_object = self.EventDBWrapper[updated_event.old.db_id]
        db_object.name = updated_event.new.name
        db_object.category_id = str(updated_event.new.category.id)
        db_object.participant_role_id = str(updated_event.new.participant_role.id)
        db_object.administrator_role_id = str(updated_event.new.administrator_role.id)

    @orm.db_session
    def delete_event(self, event:EventDiscordWrapper):
        self.EventDBWrapper[event.db_id].delete()


    async def get_all_events(self) -> list[EventDiscordWrapper]:
        events = []
        with orm.db_session:
            db_events = list(self.EventDBWrapper.select())
        for event in db_events:
            events.append(await self.get_event(event.id))
        return events

    async def get_event(self, id:int) -> EventDiscordWrapper:
        result = await self.discord_wrapper_from_db(id)
        return result
        
def get_db_instance(guild:discord.Guild) -> GuildDB:
    if not guild.id in db_instances.keys():
        db_instances[guild.id] = GuildDB(guild)
    return db_instances[guild.id]
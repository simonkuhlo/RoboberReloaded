# handles interaction with the database
from pony import orm

db = orm.Database()
db.bind(provider='sqlite', filename=f'events.sqlite', create_db=True)

class Event(db.Entity):
    guild_id = orm.Required(str)
    name = orm.Required(str)
    category_id = orm.Required(str)
    participant_role_id = orm.Required(str)
    administrator_role_id = orm.Required(str)
        
db.generate_mapping(create_tables=True)


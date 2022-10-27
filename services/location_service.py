from data.database import insert_query, read_query, update_query
from mariadb import IntegrityError
from data import database
from data.models import Location

def all(get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM cities''')

    return (Location.from_query_result(*row) for row in data)

def get_location_by_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM cities where id = ?''', (id,))

    return next((Location.from_query_result(*row) for row in data), None)

def get_location_by_name(city_name: str, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM cities where name = ?''', (city_name,))

    return next((Location.from_query_result(*row) for row in data), None)

def get_many(ids: list[int], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in ids)
    data = get_data_func(f'''SELECT * FROM cities WHERE id IN ({ids_joined})''')

    return [Location.from_query_result(*row) for row in data]    

def create_location(name: str, insert_data_func = None) -> Location | None:
    if insert_data_func is None:
        insert_data_func = database.insert_query

    try:
        generated_id = insert_data_func(
            '''INSERT INTO cities(name) VALUES (?)''', (name))
        
        return Location(id=generated_id, name=name)
    except IntegrityError:
        return None

def update_location(old: Location, new: Location, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    merged = Location(
        id=old.id,
        name=new.name or old.name
    )

    update_data_func( 
        '''UPDATE cities SET
           name = ?
           WHERE id = ? ''',
        (merged.name, merged.id))
    
    return merged

def delete_location(city_id: int, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    update_data_func('delete from cities where id = ?', (city_id,))

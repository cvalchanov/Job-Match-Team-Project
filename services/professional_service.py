from data.database import insert_query, read_query
from data.models import LoginData, Professional, ProfessionalRegisterData, ProfessionalStatus
from mariadb import IntegrityError
from common.responses import NotFound
from data import database
from services import user_service
from services import location_service

def all(status: str = None, location: str = None, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if status == ProfessionalStatus.ACTIVE:
        status = 0
    elif status == ProfessionalStatus.BUSY:
        status = 1

    if location is not None:
        city = location_service.get_location_by_name(location)
        if city is None:
            return NotFound()  

    if status is not None and location is not None:
        data = get_data_func(
            '''SELECT * FROM professionals WHERE status = ? and city_id = ?''', (status, city.id))
    elif status is not None and location is None:
        data = get_data_func(
            '''SELECT * FROM professionals WHERE status = ?''', (status,))
    elif status is None and location is not None:
        data = get_data_func(
            '''SELECT * FROM professionals WHERE city_id = ?''', (city.id,))
    else:
        data = get_data_func('''SELECT * FROM professionals''')

    return (Professional.from_query_result(*row) for row in data)

def get_many_by_id(ids: list[str], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in ids)
    data = get_data_func(f'''SELECT * FROM professionals WHERE id in ({ids_joined})''')

    return [Professional.from_query_result(*row) for row in data]

def get_many_by_city_id(city_ids: list[int], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in city_ids)
    data = get_data_func(f'''SELECT * FROM professionals WHERE city_id in ({ids_joined})''')

    return [Professional.from_query_result(*row) for row in data]

def get_professional_ads(professional_id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM professional_ads WHERE professional_id = ?''', (professional_id,))

    pass

def get_by_username(username: str, get_data_func = None) -> Professional | None:
    if get_data_func is None:
        get_data_func = database.read_query

    professional = user_service.get_by_username(username=username, table='professionals')

    return professional if professional else None

def get_by_id(id: int, get_data_func = None) -> Professional | None:
    if get_data_func is None:
        get_data_func = database.read_query

    professional = user_service.get_by_id(id=id, table='professionals')

    return professional if professional else None

def try_login(login_data: LoginData) -> Professional | None:
    professional = user_service.try_login(username=login_data.username, password=login_data.password, table='professional')

    return professional if professional else None

def create(registration_data: ProfessionalRegisterData, insert_data_func = None) -> Professional | None:
    if insert_data_func is None:
        insert_data_func = database.insert_query

    password = user_service.hash_password(registration_data.password)
    city = location_service.get_location_by_name(registration_data.location)

    try:
        generated_id = insert_data_func(
            '''INSERT INTO professionals(username, password, first_name, last_name, info, city_id) VALUES (?,?,?,?,?,?)''',
            (registration_data.username, password, registration_data.first_name, registration_data.last_name, registration_data.info, city.id))

        return Professional(
            id=generated_id,
            username=registration_data.username,
            password='',
            first_name=registration_data.first_name,
            last_name=registration_data.last_name,
            info=registration_data.info,
            city_id=city.id)
    except IntegrityError:
        return None
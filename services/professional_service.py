from data.models import LoginData, Professional, ProfessionalRegisterData, ProfessionalResponse, ProfessionalStatus, DBTable, UserType
from mariadb import IntegrityError
from common.responses import NotFound
from data import database
from services import user_service, location_service, contacts_service, professional_ad_service, match_service


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

    professional = user_service.get_by_username(username=username, table=DBTable.PROFESSIONALS)

    return professional if professional else None

def get_by_id(id: int, get_data_func = None) -> Professional | None:
    if get_data_func is None:
        get_data_func = database.read_query

    professional = user_service.get_by_id(id=id, table=DBTable.PROFESSIONALS)

    return professional if professional else None

def get_professional_email_by_id(id: int, get_data_func = None) -> str:
    if get_data_func is None:
        get_data_func = database.read_query

    email_result = get_data_func ('''select email from professional_contacts where id = ?''', (id,))
    email_stringified = email_result[0][0]
    
    return email_stringified




def try_login(login_data: LoginData) -> Professional | None:
    professional = user_service.try_login(username=login_data.username, password=login_data.password, table=DBTable.PROFESSIONALS)

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

def update(old: Professional, new: Professional, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    merged = Professional(
        id = old.id,
        username = old.username,
        password = new.password,
        first_name = new.first_name,
        last_name = new.last_name,
        info = new.info,
        status = new.status,
        city_id = new.city_id,
        main_ad = new.main_ad,
        hide_matches = new.hide_matches)

    password = user_service.hash_password(new.password)

    update_data_func(
        '''UPDATE professionals SET
        password = ?, first_name = ?, last_name = ?, info = ?, status = ?, city_id = ?, main_ad_id = ?, hide_matches = ?
        WHERE id = ?''',
        (password, merged.first_name, merged.last_name, merged.info, merged.status, merged.city_id, merged.main_ad, merged.hide_matches, merged.id))

    return merged

def change_status(id: int, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    professional = user_service.get_by_id(id=id, table=DBTable.PROFESSIONALS)

    if professional:
        if professional.status == 0:
            new_status = 1
        else:
            new_status = 0
        
        update_data_func('''UPDATE professionals SET status = ? WHERE id = ?''', (new_status, id))
        professional.status = new_status
        return professional
    else:
        return None

def create_response_object(professional: Professional):
    fullname = f'{professional.first_name} {professional.last_name}'
    location = location_service.get_location_by_id(professional.city_id)
    contacts = contacts_service.get_by_user_id(professional.id, table=DBTable.PROFESSIONAL_CONTACTS)
    active_ads_responses = professional_ad_service.get_active_ads_resps_by_user(user_id=professional.id)
    if contacts:
        contacts_response = contacts_service.create_response_object(contacts)
    else:
        contacts_response = None

    if professional.status == 0:
        status = ProfessionalStatus.ACTIVE
    else:
        status = ProfessionalStatus.BUSY

    if professional.hide_matches == 0:
        hide_matches = False
        successfull_matches = match_service.get_successfull_matches(user_id=professional.id, user_type=UserType.PROFESSIONAL)
    else:
        hide_matches = True
        successfull_matches = None


    return ProfessionalResponse(
        id = professional.id,
        fullname = fullname,
        info = professional.info,
        status = status,
        location = location.name,
        contacts = contacts_response,
        active_ads_num = len(active_ads_responses),
        active_ads_list=active_ads_responses,
        hide_matches = hide_matches,
        successfull_matches = successfull_matches)
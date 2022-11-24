from data.models import LoginData, Company, CompanyRegisterData, CompanyResponse, DBTable, UserType
from mariadb import IntegrityError
from common.responses import NotFound
from data import database
from services import user_service, location_service, contacts_service, job_ad_service, match_service


def all(name: str | None = None, location: str | None = None, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if location is not None:
        city = location_service.get_location_by_name(location)
        if city is None:
            return NotFound()

    if name is not None and location is not None:
        data = get_data_func(
            '''SELECT * FROM companies WHERE name LIKE ? and city_id = ?''', (f'%{name}%', city.id))
    elif name is not None and location is None:
        data = get_data_func(
            '''SELECT * FROM companies WHERE name LIKE ?''', (f'%{name}%',))
    elif name is None and location is not None:
        data = get_data_func(
            '''SELECT * FROM companies WHERE city_id = ?''', (city.id,))
    else:
        data = get_data_func('''SELECT * FROM companies''')

    return (Company.from_query_result(*row) for row in data)

def get_many_by_id(ids: list[int], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in ids)
    data = get_data_func(f'''SELECT * FROM companies WHERE id IN ({ids_joined})''')

    return [Company.from_query_result(*row) for row in data]

def get_many_by_city_id(city_ids: list[int], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in city_ids)
    data = get_data_func(f'''SELECT * FROM companies WHERE city_id IN ({ids_joined})''')

    return [Company.from_query_result(*row) for row in data]

def get_company_ads(company_id: int, get_data_func = None) -> list:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM job_ads WHERE company_id = ?''', (company_id,))

    pass

def get_by_name(name: str, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func('''SELECT * FROM companies WHERE name = ?''', (name,))

    return next((Company.from_query_result(*row) for row in data), None)

def get_by_username(username: str, get_data_func = None) -> Company | None:
    if get_data_func is None:
        get_data_func = database.read_query

    company = user_service.get_by_username(username=username, table=DBTable.COMPANIES)

    return company if company else None

def get_by_id(id: int, get_data_func = None) -> Company | None:
    if get_data_func is None:
        get_data_func = database.read_query

    company = user_service.get_by_id(id=id, table=DBTable.COMPANIES)

    return company if company else None

def get_company_email_by_id(id: int, get_data_func = None) -> str:
    if get_data_func is None:
        get_data_func = database.read_query

    email_result = get_data_func ('''select email from company_contacts where id = ?''', (id,))
    email_stringified = email_result[0][0]
    
    return email_stringified




def try_login(login_data: LoginData) -> Company | None:
    company = user_service.try_login(username=login_data.username, password=login_data.password, table=DBTable.COMPANIES)

    return company if company else None

def create(registration_data: CompanyRegisterData, insert_data_func = None) -> Company | None:
    if insert_data_func is None:
        insert_data_func = database.insert_query

    password = user_service.hash_password(registration_data.password)
    city = location_service.get_location_by_name(registration_data.location)

    try:
        generated_id = insert_data_func(
            '''INSERT INTO companies(username, password, name, info, city_id) VALUES (?,?,?,?,?)''',
            (registration_data.username, password, registration_data.name, registration_data.info, city.id))

        return Company(
            id=generated_id,
            username=registration_data.username,
            password='',
            name=registration_data.name,
            info=registration_data.info,
            city_id=city.id)
    except IntegrityError:
        return None

def update(old: Company, new: Company, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    merged = Company(
        id = old.id,
        username = old.username,
        password = new.password,
        name = new.name,
        info = new.info,
        city_id = new.city_id)

    password = user_service.hash_password(new.password)

    update_data_func(
        '''UPDATE companies SET
        password = ?, name = ?, info = ?, city_id = ? WHERE id = ?''',
        (password, merged.name, merged.info, merged.city_id, merged.id))

    return merged

def create_response_object(company: Company) -> CompanyResponse:
    location = location_service.get_location_by_id(company.city_id)
    contacts = contacts_service.get_by_user_id(id=company.id, table=DBTable.COMPANY_CONTACTS)
    active_ads = job_ad_service.all_active_by_company_id(id=company.id)
    active_ads_responses = [job_ad_service.create_response_object(job_ad=ja) for ja in active_ads]
    successfull_matches = match_service.get_successfull_matches(user_id=company.id, user_type=UserType.COMPANY)
    if contacts:
        contacts_response = contacts_service.create_response_object(contacts)
    else:
        contacts_response = None

    return CompanyResponse(
        id = company.id,
        name = company.name,
        info = company.info,
        location = location.name,
        contacts = contacts_response,
        active_ads_num = len(active_ads_responses),
        active_ads_list = active_ads_responses,
        successfull_matches = len(successfull_matches))

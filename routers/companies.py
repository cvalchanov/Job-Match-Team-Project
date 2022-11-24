from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import Company, CompanyRegisterData, CompanyResponse, ContactsCreationData, LoginData, DBTable
from services import company_service, user_service, contacts_service

companies_router = APIRouter(prefix='/companies')

@companies_router.post('/login')
def login(data: LoginData):
    company = user_service.try_login(username=data.username, password=data.password, table=DBTable.COMPANIES)

    if company:
        token = user_service.create_token(company)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@companies_router.post('/register')
def register(data: CompanyRegisterData):
    company = company_service.create(registration_data=data)
    if company:
        return company_service.create_response_object(company)
    else:
        return BadRequest(f'Username {data.username} is taken')

@companies_router.get('/', response_model=list[CompanyResponse])
def get_companies(name: str | None = None, location: str | None = None):
    companies = company_service.all(name=name, location=location)
    return [company_service.create_response_object(c) for c in companies]

@companies_router.get('/{id}')
def get_company_by_id(id: int):
    company = company_service.get_by_id(id)

    if company:
        return company_service.create_response_object(company)
    else:
        return NotFound()

@companies_router.put('/{id}')
def update_company(id: int, company: Company, x_token = Header()):
    logged_in_company = get_user_or_raise_401(x_token)
    target_company = company_service.get_by_id(id)

    if (logged_in_company and target_company) and logged_in_company.id == target_company.id:
        updated_company = company_service.update(old=logged_in_company, new=company)
        return company_service.create_response_object(updated_company)
    elif (logged_in_company and target_company) and logged_in_company.id != target_company.id:
        return Unauthorized()
    else:
        return NotFound()      

@companies_router.post('/{id}/contacts')
def create_company_contacts(id: int, contacts: ContactsCreationData, x_token: str = Header()):
    logged_in_company = get_user_or_raise_401(x_token)
    target_company = company_service.get_by_id(id)

    if (logged_in_company and target_company) and logged_in_company.id == target_company.id:
        contacts.user_id = logged_in_company.id
        new_contacts = contacts_service.create(contacts=contacts, table=DBTable.COMPANY_CONTACTS)
        return contacts_service.create_response_object(new_contacts)
    elif (logged_in_company and target_company) and logged_in_company.id != target_company.id:
        return Unauthorized()
    else:
        return NotFound()

@companies_router.put('/{id}/contacts')
def update_company_contacts(id: int, contacts: ContactsCreationData, x_token: str = Header()):
    logged_in_company = get_user_or_raise_401(x_token)
    target_company = company_service.get_by_id(id)
    existing_contacts = contacts_service.get_by_user_id(id, table=DBTable.COMPANY_CONTACTS)

    if (logged_in_company and target_company and existing_contacts) and logged_in_company.id == target_company.id:
        updated_contacts = contacts_service.update_contacts(old=existing_contacts, new=contacts, table=DBTable.COMPANY_CONTACTS)
        return contacts_service.create_response_object(updated_contacts)
    elif (logged_in_company and target_company and existing_contacts) and logged_in_company.id != target_company.id:
        return Unauthorized()
    else:
        return NotFound()


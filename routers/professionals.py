from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import ContactsCreationData, Professional, ProfessionalRegisterData, ProfessionalResponse, LoginData, DBTable
from services import professional_service, user_service, contacts_service

professionals_router = APIRouter(prefix='/professionals')

@professionals_router.post('/login')
def login(data: LoginData):
    professional = user_service.try_login(username=data.username, password=data.password, table=DBTable.PROFESSIONALS)

    if professional:
        token = user_service.create_token(professional)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@professionals_router.post('/register')
def register(data: ProfessionalRegisterData):
    professional = professional_service.create(registration_data=data)

    if professional:
        return professional_service.create_response_object(professional)
    else:
        return BadRequest(f'Username {data.username} is taken')

@professionals_router.get('/', response_model=list[ProfessionalResponse])
def get_professionals(status: str | None = None, location: str | None = None):
    professionals = professional_service.all(status=status, location=location)
    return [professional_service.create_response_object(p) for p in professionals]

@professionals_router.get('/{id}')
def get_professional_by_id(id: int):
    professional = professional_service.get_by_id(id)

    if professional:
        return professional_service.create_response_object(professional)
    else:
        return NotFound()

@professionals_router.put('/{id}')
def update_professional(id: int, professional: Professional, x_token = Header()):
    logged_in_professional = get_user_or_raise_401(x_token)
    target_professional = professional_service.get_by_id(id)

    if (logged_in_professional and target_professional) and logged_in_professional.id == target_professional.id:
        updated_professional = professional_service.update(old=logged_in_professional, new=professional)
        return professional_service.create_response_object(updated_professional)
    elif (logged_in_professional and target_professional) and logged_in_professional.id != target_professional.id:
        return Unauthorized()
    else:
        return NotFound()

@professionals_router.post('/{id}/contacts')
def create_professional_contacts(id: int, contacts: ContactsCreationData, x_token: str = Header()):
    logged_in_professional = get_user_or_raise_401(x_token)
    target_professional = professional_service.get_by_id(id)

    if (logged_in_professional and target_professional) and logged_in_professional.id == target_professional.id:
        contacts.user_id = logged_in_professional.id
        new_contacts = contacts_service.create(contacts=contacts, table=DBTable.PROFESSIONAL_CONTACTS)
        return contacts_service.create_response_object(new_contacts)
    elif (logged_in_professional and target_professional) and logged_in_professional.id != target_professional.id:
        return Unauthorized()
    else:
        return NotFound()

@professionals_router.put('/{id}/contacts')
def update_professional_contacts(id: int, contacts: ContactsCreationData, x_token: str = Header()):
    logged_in_professional = get_user_or_raise_401(x_token)
    target_professional = professional_service.get_by_id(id)
    existing_contacts = contacts_service.get_by_user_id(id=id, table=DBTable.PROFESSIONAL_CONTACTS)

    if (logged_in_professional and target_professional and existing_contacts) and logged_in_professional.id == target_professional.id:
        updated_contacts = contacts_service.update_contacts(old=existing_contacts, new=contacts, table=DBTable.PROFESSIONAL_CONTACTS)
        return contacts_service.create_response_object(updated_contacts)
    elif (logged_in_professional and target_professional and existing_contacts) and logged_in_professional.id != target_professional.id:
        return Unauthorized()
    else:
        return NotFound()

@professionals_router.patch('/{id}/status')
def change_professional_status(id: int, x_token: str = Header()):
    logged_in_professional = get_user_or_raise_401(x_token)
    target_professional = professional_service.get_by_id(id)

    if (logged_in_professional and target_professional) and logged_in_professional.id == target_professional.id:
        professional = professional_service.change_status(id)
        return professional_service.create_response_object(professional)
    elif (logged_in_professional and target_professional) and logged_in_professional.id != target_professional.id:
        return Unauthorized()
    else:
        return NotFound()
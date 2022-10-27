from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import Professional, ProfessionalRegisterData, ProfessionalResponse, ProfessionalMatchVisibility, LoginData, ProfessionalStatus
from services import professional_service
from services import user_service
from services import location_service

professionals_router = APIRouter(prefix='/professionals')

@professionals_router.post('/login')
def login(data: LoginData):
    professional = user_service.try_login(username=data.username, password=data.password, table='professionals')

    if professional:
        token = user_service.create_token(professional)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@professionals_router.post('/register')
def register(data: ProfessionalRegisterData):
    professional = professional_service.create(registration_data=data)

    return professional or BadRequest(f'Username {data.username} is taken')

@professionals_router.get('/', response_model=list[Professional])
def get_professionals(status: str | None = None, location: str | None = None):
    return professional_service.all(status=status, location=location)

@professionals_router.get('/{id}')
def get_professional_by_id(id: int):
    professional = professional_service.get_by_id(id)

    if professional is None:
        return NotFound()
    else:
        professional_ads = professional_service.get_professional_ads(id)
        location = location_service.get_location_by_id(professional.city_id)
        if professional.hide_matches == 0:
            match_visibility = ProfessionalMatchVisibility.VISIBLE
        else:
            match_visibility = ProfessionalMatchVisibility.HIDDEN
        if professional.status == 0:
            status = ProfessionalStatus.ACTIVE
        else:
            status = ProfessionalStatus.BUSY
        return ProfessionalResponse(
            id=professional.id,
            fullname=f'{professional.first_name} {professional.last_name}',
            info=professional.info,
            status=status,
            location=location,
            active_ads=len([ad for ad in professional_ads if ad.status == 'active']),
            match_visability=match_visibility,
            matched_ads=[ad for ad in professional_ads if ad.status == 4])
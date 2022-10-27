from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import Company, CompanyRegisterData, CompanyResponse, LoginData
from services import company_service
from services import user_service
from services import location_service

companies_router = APIRouter(prefix='/companies')

@companies_router.post('/login')
def login(data: LoginData):
    company = user_service.try_login(username=data.username, password=data.password, table='companies')

    if company:
        token = user_service.create_token(company)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@companies_router.post('/register')
def register(data: CompanyRegisterData):
    company = company_service.create(registration_data=data)

    return company or BadRequest(f'Username {data.username} is taken')

@companies_router.get('/', response_model=list[Company])
def get_companies(name: str | None = None, location: str | None = None):
    return company_service.all(name=name, location=location)

@companies_router.get('/{id}')
def get_company_by_id(id: int):
    company = company_service.get_by_id(id)

    if company is None:
        return NotFound()
    else:
        company_ads = company_service.get_company_ads(id)        
        location = location_service.get_location_by_id(company.city_id)
        return CompanyResponse(
            id=company.id,
            name=company.name,
            info=company.info,
            location=location,
            active_ads=len([ad for ad in company_ads if ad.status == 1]),
            matched_ads=len([ad for ad in company_ads if ad.status == 0]))

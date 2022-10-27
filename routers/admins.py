from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import LoginData, Admin, AdminRegisterData
from services import user_service

admins_router = APIRouter(prefix='/admins')

@admins_router.post('/login')
def login(data: LoginData):
    admin = user_service.try_login(username=data.username, password=data.password, table='admins')

    if admin:
        token = user_service.create_token(admin)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@admins_router.post('/register')
def register(data: AdminRegisterData):
    admin = user_service.create(registration_data=data)

    return admin or BadRequest(f'Username {data.username} is taken')
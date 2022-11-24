from fastapi import APIRouter
from common.responses import BadRequest
from data.models import LoginData, AdminRegisterData, DBTable
from services import user_service

admins_router = APIRouter(prefix='/admins')

@admins_router.post('/login')
def login(data: LoginData):
    admin = user_service.try_login(username=data.username, password=data.password, table=DBTable.ADMINS)

    if admin:
        token = user_service.create_token(admin)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@admins_router.post('/register')
def register(data: AdminRegisterData):
    admin = user_service.create(registration_data=data)

    return admin or BadRequest(f'Username {data.username} is taken')
import unittest
from unittest.mock import Mock
from data.models import Admin, Professional, Company, LoginData, AdminRegisterData, UserType
from routers import admins as admins_router
from common.responses import BadRequest
import jwt
from datetime import datetime, timedelta

SECRET = 'the sky is blue'
mock_user_service = Mock('services.user_service')

admins_router.user_service = mock_user_service

def fake_admin(id=1, username="admin", password="password"):
    mock_admin = Mock(spec=Admin)
    mock_admin.id = id
    mock_admin.username = username
    mock_admin.password = password
    return mock_admin

def fake_company(id=1, username="company", password="password", name="company name", info="company info", city_id=1):
    mock_company = Mock(spec=Company)
    mock_company.id = id
    mock_company.username = username
    mock_company.password = password
    mock_company.name = name
    mock_company.info = info
    mock_company.city_id = city_id
    return mock_company

def fake_professional(id=1, username="professional", password="password", first_name="firstname", last_name="lastname",
    info="professional info", status=0, city_id=1, main_ad=None, hide_matches=0):
    mock_professional = Mock(spec=Professional)
    mock_professional.id = id
    mock_professional.username = username
    mock_professional.password = password
    mock_professional.first_name = first_name
    mock_professional.last_name = last_name
    mock_professional.info = info
    mock_professional.status = status
    mock_professional.city_id = city_id
    mock_professional.main_ad = main_ad
    mock_professional.hide_matches = hide_matches
    return mock_professional

class AdminsRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_user_service.reset_mock()

    def test_login_returns_token_whenUser(self):
        data = LoginData(username='admin', password='password')
        admin = fake_admin()
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': admin.id, 'username': admin.username, 'type': UserType.ADMIN}, SECRET, algorithm='HS256')
        mock_user_service.try_login = lambda username, password, table: admin
        mock_user_service.create_token = lambda user: token
        expected = {'token': token}
        result = admins_router.login(data=data)

        self.assertEqual(expected, result)
    
    def test_login_returns_BadRequest_whenNoUser(self):
        data = LoginData(username='admin', password='password')
        mock_user_service.try_login = lambda username, password, table: None

        self.assertEqual(BadRequest, type(admins_router.login(data=data)))

    def test_register_returns_Admin_when_usernameIsFree(self):
        data = AdminRegisterData(username='admin', password='password')
        admin = fake_admin()
        mock_user_service.create = lambda registration_data: admin

        self.assertEqual(admin, admins_router.register(data=data))

    def test_register_returns_BadRequest_when_usernameTaken(self):
        data = AdminRegisterData(username='admin', password='password')
        mock_user_service.create = lambda registration_data: None

        self.assertEqual(BadRequest, type(admins_router.register(data=data)))
import unittest
import jwt
from data.models import Admin, Company, Professional, AdminRegisterData, UserType
from services import user_service
from mariadb import IntegrityError
from datetime import datetime, timedelta

class UserService_Should(unittest.TestCase):

    def test_getByUsername_returns_None_whenNoUser(self):
        get_data_func = lambda q, username: []

        self.assertEqual(None, user_service.get_by_username(username='username', table='companies', get_data_func=get_data_func))

    def test_getByUsername_returns_Admin_whenThereIsOne(self):
        get_data_func = lambda q, username: [(1, 'admin', 'password')]

        expected = Admin(id=1, username='admin', password='password')
        result = user_service.get_by_username(username='admin', table='admins', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByUsername_returns_Company_whenThereIsOne(self):
        get_data_func = lambda q, username: [(1, 'company', 'password', 'name', 'info', 1)]

        expected = Company(id=1, username='company', password='password', name='name', info='info', city_id=1)
        result = user_service.get_by_username(username='company', table='companies', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByUsername_returns_Professional_whenThereIsOne(self):
        get_data_func = lambda q, username: [(1, 'professional', 'password', 'firstname', 'lastname', 'info', 0, 1, None, 0)]

        expected = Professional(id=1, username='professional', password='password', first_name='firstname', last_name='lastname',
            info='info', status=0, city_id=1, main_ad=None, hide_matches=0)
        result = user_service.get_by_username(username='professional', table='professionals', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByID_returns_None_whenNoUser(self):
        get_data_func = lambda q, id: []

        self.assertEqual(None, user_service.get_by_id(id=1, table='companies', get_data_func=get_data_func))

    def test_getByID_returns_Admin_whenThereIsOne(self):
        get_data_func = lambda q, id: [(1, 'admin', 'password')]

        expected = Admin(id=1, username='admin', password='password')
        result = user_service.get_by_id(id=1, table='admins', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByID_returns_Company_whenThereIsOne(self):
        get_data_func = lambda q, id: [(1, 'company', 'password', 'name', 'info', 1)]

        expected = Company(id=1, username='company', password='password', name='name', info='info', city_id=1)
        result = user_service.get_by_id(id=1, table='companies', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByID_returns_Professional_whenThereIsOne(self):
        get_data_func = lambda q, id: [(1, 'professional', 'password', 'firstname', 'lastname', 'info', 0, 1, None, 0)]

        expected = Professional(id=1, username='professional', password='password', first_name='firstname', last_name='lastname',
            info='info', status=0, city_id=1, main_ad=None, hide_matches=0)
        result = user_service.get_by_id(id=1, table='professionals', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_create_returns_Admin_when_noError(self):
        insert_data_func = lambda q, a: 1
        register_data = AdminRegisterData(username='admin', password='password')

        expected = Admin(id=1, username='admin', password='')
        result = user_service.create(registration_data=register_data, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)
    
    def test_create_returns_None_whenError(self):
        def insert_data_func(q, a):
            raise IntegrityError

        register_data = AdminRegisterData(username='admin', password='password')

        self.assertEqual(None, user_service.create(registration_data=register_data, insert_data_func=insert_data_func))

    def test_createToken_creates_adminToken(self):
        admin = Admin(id=1, username='admin', password='password')
        token_expiration = datetime.now() + timedelta(days=14)
        expected = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'admin', 'type': UserType.ADMIN}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(expected, user_service.create_token(admin))

    def test_decodeToken_returns_userInfo_when_TokenIsValid(self):
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'admin', 'type': UserType.ADMIN}, user_service.SECRET, algorithm="HS256")

        expected = jwt.decode(token, user_service.SECRET, algorithms=["HS256"])

        self.assertEqual(expected, user_service.decode_token(token))

    def test_decodeToken_returns_None_when_TokenIsInvalid(self):
        token = 'this_token_is_invalid'

        self.assertEqual(None, user_service.decode_token(token))

    def test_isAuthenticated_returns_None_when_InvalidToken(self):
        token = 'this_token_is_invalid'

        self.assertEqual(None, user_service.is_authenticated(token))

    def test_isAuthenticated_returns_True_when_thereIsAdmin(self):
        get_data_func = lambda q, a: [(1, 'admin', 'password')]
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'admin', 'type': UserType.ADMIN}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(True, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    def test_isAuthenticated_returns_True_when_thereIsCompany(self):
        get_data_func = lambda q, a: [(1, 'company', 'password', 'name', 'info', 1)]
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'company', 'type': UserType.COMPANY}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(True, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    def test_isAuthenticated_returns_True_when_thereIsProfessional(self):
        get_data_func = lambda q, a: [(1, 'professional', 'password', 'firstname', 'lastname', 'info', 0, 1, None, 0)]
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'professional', 'type': UserType.PROFESSIONAL}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(True, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    def test_isAuthenticated_returns_False_when_noAdmin(self):
        get_data_func = lambda q, a: []
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'admin', 'type': UserType.ADMIN}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(False, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    def test_isAuthenticated_returns_False_when_noCompany(self):
        get_data_func = lambda q, a: []
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'company', 'type': UserType.COMPANY}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(False, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    def test_isAuthenticated_returns_False_when_noProfessional(self):
        get_data_func = lambda q, a: []
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': 1, 'username': 'professional', 'type': UserType.PROFESSIONAL}, user_service.SECRET, algorithm="HS256")

        self.assertEqual(False, user_service.is_authenticated(token=token, get_data_func=get_data_func))

    
import unittest
from unittest.mock import Mock
from data.models import Professional, ProfessionalRegisterData, ProfessionalResponse, LoginData, Contacts, ContactsResponse, UserType
from routers import professionals as professionals_router
from common.responses import NotFound, BadRequest, Unauthorized
import jwt
from datetime import datetime, timedelta

SECRET = 'the sky is blue'
mock_user_service = Mock('services.user_service')
mock_professional_service = Mock('services.professional_service')
mock_contacts_service = Mock('services.contacts_service')
mock_auth = Mock()
professionals_router.user_service = mock_user_service
professionals_router.professional_service = mock_professional_service
professionals_router.contacts_service = mock_contacts_service
professionals_router.get_user_or_raise_401 = mock_auth

def fake_professional(id=1, username='pro', password='password', first_name='firstname',
    last_name='lastname', info='info', status=0, city_id=1, main_ad=1, hide_matches=0):
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

def fake_contacts(id=1, phone_number='1111', email='email', website='website',
    linkedin='linkedin', facebook='facebook', twitter='twitter', user_id=1):
    mock_contacts = Mock(spec=Contacts)
    mock_contacts.id = id
    mock_contacts.phone_number = phone_number
    mock_contacts.email = email
    mock_contacts.website = website
    mock_contacts.linkedin = linkedin
    mock_contacts.facebook = facebook
    mock_contacts.twitter = twitter
    mock_contacts.user_id = user_id
    return mock_contacts

class ProfessionalsRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_contacts_service.reset_mock()
        mock_professional_service.reset_mock()
        mock_user_service.reset_mock()
        mock_auth.reset_mock()

    def test_login_returns_token_whenProfessional(self):
        data = LoginData(username='pro', password='password')
        professional = fake_professional()
        token_expiration = datetime.now() + timedelta(hours=9)
        token = jwt.encode({'exp': token_expiration, 'id': professional.id, 'username': professional.username,
            'type': UserType.PROFESSIONAL}, SECRET, algorithm='HS256')
        mock_user_service.try_login = lambda username, password, table: professional
        mock_user_service.create_token = lambda user: token
        expected = {'token': token}
        result = professionals_router.login(data=data)

        self.assertEqual(expected, result)

    def test_login_returns_BadRequest_whenNoProfessional(self):
        data = LoginData(username='pro', password='password')
        mock_user_service.try_login = lambda username, password, table: None

        self.assertEqual(BadRequest, type(professionals_router.login(data=data)))

    def test_register_returns_Professional_when_usernameIsFree(self):
        data = ProfessionalRegisterData(username='pro', password='password', first_name='firstname',
            last_name='lastname', info='info', location='city')
        professional = fake_professional()
        professional_response = ProfessionalResponse(id=1, fullname=f'{data.first_name} {data.last_name}',
            info=data.info, status='active', location=data.location, contacts=None, active_ads_num=0,
            active_ads_list=[], hide_matches=False, successfull_matches=[])
        mock_professional_service.create = lambda registration_data: professional
        mock_professional_service.create_response_object = lambda professional: professional_response

        self.assertEqual(professional_response, professionals_router.register(data=data))

    def test_register_returns_BadRequest_when_usernameTaken(self):
        data = ProfessionalRegisterData(username='pro', password='password', first_name='firstname',
            last_name='lastname', info='info', location='city')
        mock_professional_service.create = lambda registration_data: None

        self.assertEqual(BadRequest, type(professionals_router.register(data=data)))

    def test_getProfessionals_returns_listOfProfessionalReponseObjects_when_dataIsPresent(self):
        professional = fake_professional()
        professional_response = ProfessionalResponse(
            id=professional.id, fullname=f'{professional.first_name} {professional.last_name}', info=professional.info,
            status='active', location='city', contacts=None, active_ads_num=0, active_ads_list=[], hide_matches=False, successfull_matches=[])
        mock_professional_service.all = lambda status, location: [professional]
        mock_professional_service.create_response_object = lambda professional: professional_response

        self.assertEqual([professional_response], professionals_router.get_professionals())

    def test_getProfessionals_returns_emptyList_when_noData(self):
        mock_professional_service.all = lambda status, location: []

        self.assertEqual([], professionals_router.get_professionals())

    def test_getProfessionalById_returns_ProfessionalResponseObject_when_found(self):
        professional = fake_professional()
        professional_response = ProfessionalResponse(
            id=professional.id, fullname=f'{professional.first_name} {professional.last_name}', info=professional.info,
            status='active', location='city', contacts=None, active_ads_num=0, active_ads_list=[], hide_matches=False, successfull_matches=[])
        mock_professional_service.get_by_id = lambda id: professional
        mock_professional_service.create_response_object = lambda professional: professional_response

        self.assertEqual(professional_response, professionals_router.get_professional_by_id(1))

    def test_getProfessionalById_returns_NotFound_when_noProfessional(self):
        mock_professional_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(professionals_router.get_professional_by_id(1)))

    def test_updateProfessional_returns_ProfessionalResponseObject_when_successful(self):
        professional = fake_professional()
        professional_response = ProfessionalResponse(
            id=professional.id, fullname=f'{professional.first_name} {professional.last_name}', info=professional.info,
            status='active', location='city', contacts=None, active_ads_num=0, active_ads_list=[], hide_matches=False, successfull_matches=[])
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: professional
        mock_professional_service.update = lambda old, new: professional
        mock_professional_service.create_response_object = lambda professional: professional_response

        self.assertEqual(professional_response, professionals_router.update_professional(id=1, professional=professional))

    def test_updateProfessional_returns_Unauthorized_when_loggedInProfessional_differentFrom_targetProfessional(self):
        pro1 = fake_professional()
        pro2 = fake_professional(id=2)
        mock_auth.return_value = pro1
        mock_professional_service.get_by_id = lambda id: pro2

        self.assertEqual(Unauthorized, type(professionals_router.update_professional(2, professional=pro1)))

    def test_updateProfessional_returns_NotFound_when_noProfessionalFound(self):
        professional = fake_professional()
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(professionals_router.update_professional(2, professional=professional)))

    def test_createProfessionalContacts_returns_contactsResponseObject_when_successful(self):
        professional = fake_professional()
        contacts = fake_contacts()
        contacts_response = ContactsResponse(phone_number=contacts.phone_number, email=contacts.email,
            website=contacts.website, linkedin=contacts.linkedin, facebook=contacts.facebook, twitter=contacts.twitter)
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: professional
        mock_contacts_service.create = lambda contacts, table: contacts
        mock_contacts_service.create_response_object = lambda contacts: contacts_response

        self.assertEqual(contacts_response, professionals_router.create_professional_contacts(1, contacts=contacts))

    def test_createProfessionalContacts_returns_Unauthorized_when_loggedInProfessional_differentFrom_targetProfessional(self):
        pro1 = fake_professional()
        pro2 = fake_professional(id=2)
        contacts = fake_contacts()
        mock_auth.return_value = pro1
        mock_professional_service.get_by_id = lambda id: pro2

        self.assertEqual(Unauthorized, type(professionals_router.create_professional_contacts(2, contacts=contacts)))

    def test_createProfessionalContacts_returns_NotFound_when_noProfessionalFound(self):
        professional = fake_professional()
        contacts = fake_contacts()
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(professionals_router.create_professional_contacts(2, contacts=contacts)))

    def test_updateProfessionalContacts_returns_contactsResponseObject_when_successful(self):
        professional = fake_professional()
        contacts = fake_contacts()
        contacts_response = ContactsResponse(phone_number=contacts.phone_number, email=contacts.email,
            website=contacts.website, linkedin=contacts.linkedin, facebook=contacts.facebook, twitter=contacts.twitter)
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: professional
        mock_contacts_service.get_by_user_id = lambda id, table: contacts
        mock_contacts_service.update_contacts = lambda old, new, table: contacts
        mock_contacts_service.create_response_object = lambda contacts: contacts_response

        self.assertEqual(contacts_response, professionals_router.update_professional_contacts(1, contacts=contacts))

    def test_updateProfessionalContacts_returns_Unauthorized_when_loggedInProfessional_differentFrom_targetProfessional(self):
        pro1 = fake_professional()
        pro2 = fake_professional(id=2)
        contacts = fake_contacts()
        mock_auth.return_value = pro1
        mock_professional_service.get_by_id = lambda id: pro2
        mock_contacts_service.get_by_user_id = lambda id, table: contacts

        self.assertEqual(Unauthorized, type(professionals_router.update_professional_contacts(2, contacts=contacts)))

    def test_updateProfessionalContacts_returns_NotFound_when_noProfessionalFound(self):
        professional = fake_professional()
        contacts = fake_contacts()
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: None
        mock_contacts_service.get_by_user_id = lambda id, table: contacts

        self.assertEqual(NotFound, type(professionals_router.update_professional_contacts(1, contacts=contacts)))

    def test_changeProfessionalStatus_returns_professionalResponseObject_when_successful(self):
        professional = fake_professional()
        professional_response = ProfessionalResponse(
            id=professional.id, fullname=f'{professional.first_name} {professional.last_name}', info=professional.info,
            status='active', location='city', contacts=None, active_ads_num=0, active_ads_list=[], hide_matches=False, successfull_matches=[])
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: professional
        mock_professional_service.change_status = lambda id: professional
        mock_professional_service.create_response_object = lambda professional: professional_response

        self.assertEqual(professional_response, professionals_router.change_professional_status(1))

    def test_changeProfessionalStatus_returns_Unauthorized_when_loggedInProfessional_differentFrom_targetProfessional(self):
        pro1 = fake_professional()
        pro2 = fake_professional(id=2)
        mock_auth.return_value = pro1
        mock_professional_service.get_by_id = lambda id: pro2

        self.assertEqual(Unauthorized, type(professionals_router.change_professional_status(2)))

    def test_changeProfessionalStatus_returns_NotFound_when_noProfessionalFound(self):
        professional = fake_professional()
        mock_auth.return_value = professional
        mock_professional_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(professionals_router.change_professional_status(1)))
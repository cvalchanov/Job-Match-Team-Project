import unittest
from unittest.mock import Mock
from data.models import Professional, ProfessionalRegisterData, ProfessionalResponse, Location, LoginData, Contacts, ContactsResponse
from services import professional_service
from mariadb import IntegrityError
from common.responses import NotFound

mock_user_service = Mock('services.user_service')
mock_location_service = Mock('services.location_service')
mock_contacts_service = Mock('services.contacts_service')
mock_professional_ad_service = Mock('service.professional_ad_service')
mock_match_service = Mock('services.match_service')
professional_service.user_service = mock_user_service
professional_service.location_service = mock_location_service
professional_service.contacts_service = mock_contacts_service
professional_service.professional_ad_service = mock_professional_ad_service
professional_service.match_service = mock_match_service

class ProfessionalService_Should(unittest.TestCase):

    def setUp(self):
        mock_location_service.reset_mock()
        mock_user_service.reset_mock()
        mock_contacts_service.reset_mock()
        mock_professional_ad_service.reset_mock()
        mock_match_service.reset_mock()

    def test_all_returns_emptyList_when_noProfessionals(self):
        get_data_func = lambda q: []

        self.assertEqual([], list(professional_service.all(get_data_func=get_data_func)))

    def test_all_returns_listOfProfessionals(self):
        get_data_func = lambda q: [(1, 'pro1', 'pass1', 'firstname1', 'lastname1', 'info1', 0, 1, 1, 0),
        (2, 'pro2', 'pass2', 'firstname2', 'lastname2', 'info2', 0, 1, 1, 0)]
        expected = [
            Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
            last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0),
            Professional(id=2, username='pro2', password='pass2', first_name='firstname2', 
            last_name='lastname2', info='info2', status=0, city_id=1, main_ad=1, hide_matches=0),]
        result = list(professional_service.all(get_data_func=get_data_func))

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_all_returns_NotFound_when_noCity(self):
        mock_location_service.get_location_by_name = lambda location: None

        self.assertEqual(NotFound, type(professional_service.all(location='city')))

    def test_getManyById_returns_emptyList_when_noData(self):
        get_data_func = lambda q: []

        self.assertEqual([], professional_service.get_many_by_id(ids=[], get_data_func=get_data_func))

    def test_getManyById_returns_listOfProfessionals_when_dataIsPresent(self):
        get_data_func = lambda q: [(1, 'pro1', 'pass1', 'firstname1', 'lastname1', 'info1', 0, 1, 1, 0),
        (2, 'pro2', 'pass2', 'firstname2', 'lastname2', 'info2', 0, 1, 1, 0)]
        expected = [
            Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
            last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0),
            Professional(id=2, username='pro2', password='pass2', first_name='firstname2', 
            last_name='lastname2', info='info2', status=0, city_id=1, main_ad=1, hide_matches=0),]
        result = professional_service.get_many_by_id(ids=[1,2], get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_getManyByCItyId_returns_emptyList_when_noData(self):
        get_data_func = lambda q: []

        self.assertEqual([], professional_service.get_many_by_city_id(city_ids=[], get_data_func=get_data_func))

    def test_getManyByCityId_returns_listOfProfessionals_when_dataIsPresent(self):
        get_data_func = lambda q: [(1, 'pro1', 'pass1', 'firstname1', 'lastname1', 'info1', 0, 1, 1, 0),
        (2, 'pro2', 'pass2', 'firstname2', 'lastname2', 'info2', 0, 1, 1, 0)]
        expected = [
            Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
            last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0),
            Professional(id=2, username='pro2', password='pass2', first_name='firstname2', 
            last_name='lastname2', info='info2', status=0, city_id=1, main_ad=1, hide_matches=0),]
        result = professional_service.get_many_by_city_id(city_ids=[1,2], get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_getByUsername_returns_Professional_when_thereIsOne(self):
        professional = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
        last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0)
        mock_user_service.get_by_username = lambda username, table: professional

        self.assertEqual(professional, professional_service.get_by_username(username='pro1'))

    def test_getByUsername_returns_None_when_noProfessional(self):
        mock_user_service.get_by_username = lambda username, table: None

        self.assertEqual(None, professional_service.get_by_username(username='pro1'))

    def test_getById_returns_Professional_when_thereIsOne(self):
        professional = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
        last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0)
        mock_user_service.get_by_id = lambda id, table: professional

        self.assertEqual(professional, professional_service.get_by_id(id=1))

    def test_getById_returns_None_when_noProfessional(self):
        mock_user_service.get_by_id = lambda id, table: None

        self.assertEqual(None, professional_service.get_by_id(id=1))

    def test_tryLogin_returns_Professional_when_thereIsOne(self):
        login_data = LoginData(username='pro1', password='pass1')
        professional = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
        last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0)
        mock_user_service.try_login = lambda username, password, table: professional

        self.assertEqual(professional, professional_service.try_login(login_data=login_data))

    def test_tryLogin_returns_None_when_noProfessional(self):
        login_data = LoginData(username='pro1', password='pass1')
        mock_user_service.try_login = lambda username, password, table: None

        self.assertEqual(None, professional_service.try_login(login_data=login_data))

    def test_create_returns_Professional_when_NoError(self):
        insert_data_func = lambda q, a: 1
        city = Location(id=1, name='location1')
        registration_data = ProfessionalRegisterData(username='pro1', password='pass1', first_name='firstname1', 
                                                        last_name='lastname1', info='info1', location='location1')
        mock_user_service.hash_password = lambda password: ''
        mock_location_service.get_location_by_name = lambda location: city

        expected = Professional(id=1, username='pro1', password='', first_name='firstname1', last_name='lastname1',
                                                    info='info1', status=0, city_id=1, main_ad=None, hide_matches=0)

        result = professional_service.create(registration_data=registration_data, insert_data_func=insert_data_func)
        
        self.assertEqual(expected, result)

    def test_create_returns_None_whenError(self):
        def insert_data_func(q, a):
            raise IntegrityError
        city = Location(id=1, name='location1')
        registration_data = ProfessionalRegisterData(username='pro1', password='pass1', first_name='firstname1', 
                                                        last_name='lastname1', info='info1', location='location1')
        mock_user_service.hash_password = lambda password: ''
        mock_location_service.get_location_by_name = lambda location: city

        self.assertEqual(None, professional_service.create(registration_data=registration_data, insert_data_func=insert_data_func))

    def test_update_returns_updatedProfessional(self):
        update_data_func = lambda q, a: None
        old = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
            last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0)
        new = Professional(id=2, username='pro2', password='pass2', first_name='firstname2', 
            last_name='lastname2', info='info2', status=1, city_id=2, main_ad=2, hide_matches=1)
        mock_user_service.hash_password = lambda q: ''

        expected = Professional(id=1, username='pro1', password='pass2', first_name='firstname2',
            last_name='lastname2', info='info2', status=1, city_id=2, main_ad=2, hide_matches=1)
        result = professional_service.update(old=old, new=new, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_changeStatus_returns_Professional_with_changedStatus(self):
        update_data_func = lambda q, a: None
        professional = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
        last_name='lastname1', info='info1', status=0, city_id=1, main_ad=1, hide_matches=0)        
        mock_user_service.get_by_id = lambda id, table: professional
        professional.status = 1

        self.assertEqual(professional, professional_service.change_status(id=1, update_data_func=update_data_func))

    def test_changeStatus_returns_None_whenNoProfessional(self):
        update_data_func = lambda q, a: None        
        mock_user_service.get_by_id = lambda id, table: None

        self.assertEqual(None, professional_service.change_status(id=1, update_data_func=update_data_func))

    def test_createResponseObject_returns_ProfessionalResponse(self):
        professional = Professional(id=1, username='pro1', password='pass1', first_name='firstname1', 
                                    last_name='lastname1', info='info1', status=0, city_id=1, main_ad=0, hide_matches=0)
        location = Location(id=1, name='location1')
        contacts = Contacts(id=1, phone_number='0000', email='email', website='website', 
                            linkedin='linkedin', facebook='facebook', twitter='twitter', user_id=1)
        contacts_response = ContactsResponse(phone_number='0000', email='email', website='website', 
                                                linkedin='linkedin', facebook='facebook', twitter='twitter')
        mock_location_service.get_location_by_id = lambda q: location
        mock_contacts_service.get_by_user_id = lambda id, table: contacts
        mock_contacts_service.create_response_object = lambda contacts: contacts_response
        mock_professional_ad_service.get_active_ads_resps_by_user = lambda user_id: []
        mock_match_service.get_successfull_matches = lambda user_id, user_type: []

        expected = ProfessionalResponse(id=1, fullname=f'{professional.first_name} {professional.last_name}', info='info1',
            status='active', location='location1', contacts=contacts_response, active_ads_num=0, active_ads_list=[], hide_matches=False, successfull_matches=[])
        result = professional_service.create_response_object(professional=professional)

        self.assertEqual(expected, result)
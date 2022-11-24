import unittest
from unittest.mock import Mock
from data.models import Company, CompanyRegisterData, CompanyResponse, Location, LoginData, Contacts, ContactsResponse
from services import company_service
from mariadb import IntegrityError
from common.responses import NotFound

mock_user_service = Mock('services.user_service')
mock_location_service = Mock('services.location_service')
mock_contacts_service = Mock('services.contacts_service')
mock_job_ad_service = Mock('services.job_ad_service')
mock_match_service = Mock('services.match_service')
company_service.user_service = mock_user_service
company_service.location_service = mock_location_service
company_service.contacts_service = mock_contacts_service
company_service.job_ad_service = mock_job_ad_service
company_service.match_service = mock_match_service

class CompanyService_Should(unittest.TestCase):

    def setUp(self):
        mock_user_service.reset_mock()
        mock_location_service.reset_mock()
        mock_contacts_service.reset_mock()
        mock_job_ad_service.reset_mock()
        mock_match_service.reset_mock()

    def test_all_returns_emptyList_when_noCompanies(self):
        get_data_func = lambda q: []

        self.assertEqual([], list(company_service.all(get_data_func=get_data_func)))

    def test_all_returns_listOfCompanies(self):
        get_data_func = lambda q: [(1, 'comp1', 'pass1', 'name1', 'info1', 1), (2, 'comp2', 'pass2', 'name2', 'info2', 2)]

        expected = [Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1),
                    Company(id=2, username='comp2', password='pass2', name='name2', info='info2', city_id=2)]

        result = list(company_service.all(get_data_func=get_data_func))

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_all_returns_NotFound_when_noCity(self):
        mock_location_service.get_location_by_name = lambda location: None

        self.assertEqual(NotFound, type(company_service.all(location='city')))

    def test_get_many_by_id_returns_listOfCompanies_when_dataIsPresent(self):
        get_data_func = lambda q: [(1, 'comp1', 'pass1', 'name1', 'info1', 1), (2, 'comp2', 'pass2', 'name2', 'info2', 2)]

        expected = [Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1),
                    Company(id=2, username='comp2', password='pass2', name='name2', info='info2', city_id=2)]

        result = company_service.get_many_by_id(ids=[1,2], get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_get_many_by_id_returns_emptyList_when_noData(self):
        get_data_func = lambda q: []

        self.assertEqual([], company_service.get_many_by_id(ids=[], get_data_func=get_data_func))

    def test_get_many_by_city_id_returns_emptyList_when_noData(self):
        get_data_func = lambda q: []

        self.assertEqual([], company_service.get_many_by_city_id(city_ids=[], get_data_func=get_data_func))

    def test_get_many_by_city_id_returns_listOfCompanies_when_dataIsPresent(self):
        get_data_func = lambda q: [(1, 'comp1', 'pass1', 'name1', 'info1', 1), (2, 'comp2', 'pass2', 'name2', 'info2', 2)]

        expected = [Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1),
                    Company(id=2, username='comp2', password='pass2', name='name2', info='info2', city_id=2)]

        result = company_service.get_many_by_city_id(city_ids=[1,2], get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_get_by_name_returns_Company_when_thereIsOne(self):
        company = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)
        get_data_func = lambda a,b: [(1, 'comp1', 'pass1', 'name1', 'info1', 1)]

        self.assertEqual(company, company_service.get_by_name(name='comp1', get_data_func=get_data_func))

    def test_get_by_name_returns_None_when_noData(self):
        get_data_func = lambda a,b: []

        self.assertEqual(None, company_service.get_by_name(name='comp1', get_data_func=get_data_func))

    def test_get_by_username_returns_Company_when_thereIsOne(self):
        company = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)

        mock_user_service.get_by_username = lambda username, table: company

        self.assertEqual(company, company_service.get_by_username(username='comp1'))

    def test_get_by_username_returns_None_when_noData(self):
        mock_user_service.get_by_username = lambda username, table: None

        self.assertEqual(None, company_service.get_by_username(username='comp1'))

    def test_get_by_id_returns_None_when_noData(self):
        mock_user_service.get_by_id = lambda id, table: None

        self.assertEqual(None, company_service.get_by_id(id=1))

    def test_get_by_id_returns_Company_when_thereIsOne(self):
        company = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)

        mock_user_service.get_by_id = lambda id, table: company

        self.assertEqual(company, company_service.get_by_id(id=1))

    def test_tryLogin_returns_company_when_thereIsOne(self):
        data = LoginData(username='comp1', password='pass1')
        company = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)

        mock_user_service.try_login = lambda username, password, table: company

        self.assertEqual(company, company_service.try_login(login_data=data))

    def test_try_login_returns_None_when_noCompany(self):
        data = LoginData(username='comp1', password='pass1')

        mock_user_service.try_login = lambda username, password, table: None

        self.assertEqual(None, company_service.try_login(login_data=data))

    def test_create_returns_Company_when_usernameIsFree(self):
        data = CompanyRegisterData(username='comp1', password='pass1', name='name1', info='info1', location='city1')
        location = Location(id=1, name='city1')

        insert_data_func = lambda q,a: 1
        mock_user_service.hash_password = lambda q: 'pass1'
        mock_location_service.get_location_by_name = lambda q: location
        expected = Company(id=1, username='comp1', password='', name='name1', info='info1', city_id=1)
        result = company_service.create(registration_data=data, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)

    def test_create_returns_None_when_usernameTaken(self):
        def insert_data_func(q, a):
            raise IntegrityError

        data = CompanyRegisterData(username='comp1', password='pass1', name='name1', info='info1', location='city1')
        location = Location(id=1, name='city1')

        mock_user_service.hash_password = lambda q: 'pass1'
        mock_location_service.get_location_by_name = lambda q: location

        self.assertEqual(None, company_service.create(registration_data=data, insert_data_func=insert_data_func))

    def test_update_returns_updated_company(self):
        comp1 = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)
        comp2 = Company(id=2, username='comp2', password='pass2', name='name2', info='info2', city_id=2)
        expected = Company(id=1, username='comp1', password='pass2', name='name2', info='info2', city_id=2)
        update_data_func = lambda q,a: None
        mock_user_service.hash_password = lambda q: ''

        result = company_service.update(old=comp1, new=comp2, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_create_response_object_returns_companyResponseObject(self):
        comp1 = Company(id=1, username='comp1', password='pass1', name='name1', info='info1', city_id=1)
        contacts = Contacts(id=1, phone_number='111', email='email1', website='website1', linkedin='linkedin1', facebook='facebook1', twitter='twitter1', user_id=1)
        contacts_response = ContactsResponse(phone_number='111', email='email1', website='website1', linkedin='linkedin1', facebook='facebook1', twitter='twitter1')
        location = Location(id=1, name='city1')
        mock_location_service.get_location_by_id = lambda id: location
        mock_contacts_service.get_by_user_id = lambda id, table: contacts
        mock_contacts_service.create_response_object = lambda c: contacts_response
        mock_job_ad_service.all_active_by_company_id = lambda id: []
        mock_job_ad_service.create_response_object = lambda ad: []
        mock_match_service.get_successfull_matches = lambda user_id, user_type: []

        expected = CompanyResponse(id=comp1.id, name=comp1.name, info=comp1.info, location=location.name,
            contacts=contacts_response, active_ads_num=0, active_ads_list=[], successfull_matches=0)
        result = company_service.create_response_object(company=comp1)
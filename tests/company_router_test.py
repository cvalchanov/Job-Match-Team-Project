import unittest
from unittest.mock import Mock
from data.models import Company, CompanyRegisterData, CompanyResponse, LoginData, Contacts, ContactsResponse
from routers import companies as companies_router
from common.responses import NotFound, BadRequest, Unauthorized

SECRET = 'the sky is blue'
mock_user_service = Mock('services.user_service')
mock_company_service = Mock('services.company_service')
mock_contacts_service = Mock('services.contacts_service')
mock_auth = Mock()
companies_router.user_service = mock_user_service
companies_router.company_service = mock_company_service
companies_router.contacts_service = mock_contacts_service
companies_router.get_user_or_raise_401 = mock_auth

def fake_company(id=1, username='comp', password='password', name='name', info='info', city_id=1):
    mock_company = Mock(spec=Company)
    mock_company.id = id
    mock_company.username = username
    mock_company.password = password
    mock_company.name = name
    mock_company.info = info
    mock_company.city_id = city_id
    return mock_company

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

class CompaniesRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_user_service.reset_mock()
        mock_company_service.reset_mock()
        mock_contacts_service.reset_mock()
        mock_auth.reset_mock()

    def test_login_returns_token_whenCompany(self):
        data = LoginData(username='comp', password='password')
        company = fake_company()
        token = 'token'
        mock_user_service.try_login = lambda username, password, table: company
        mock_user_service.create_token = lambda user: token
        expected = {'token': token}
        result = companies_router.login(data=data)

        self.assertEqual(expected, result)

    def test_login_returns_BadRequest_whenNoCompany(self):
        data = LoginData(username='comp', password='password')
        mock_user_service.try_login = lambda username, password, table: None

        self.assertEqual(BadRequest, type(companies_router.login(data=data)))

    def test_register_returns_Company_when_usernameIsFree(self):
        data = CompanyRegisterData(username='comp', password='password', name='name', info='info', location='city')
        company = fake_company()
        company_response = CompanyResponse(id=1, name=data.name, info=data.info, location=data.location, contacts=None,
            active_ads_num=0, active_ads_list=[], successfull_matches=0)
        mock_company_service.create = lambda registration_data: company
        mock_company_service.create_response_object = lambda comp: company_response

        self.assertEqual(company_response, companies_router.register(data=data))

    def test_register_returns_BadRequest_when_usernameTaken(self):
        data = CompanyRegisterData(username='comp', password='password', name='name', info='info', location='city')
        mock_company_service.create = lambda registration_data: None

        self.assertEqual(BadRequest, type(companies_router.register(data=data)))

    def test_getCompanies_returns_list_of_CompanyResponseObjects_when_dataIsPresent(self):
        company = fake_company()
        company_response = CompanyResponse(id=1, name='name', info='info', location='city', contacts=None,
            active_ads_num=0, active_ads_list=[], successfull_matches=0)

        mock_company_service.all = lambda name, location: [company]
        mock_company_service.create_response_object = lambda company: company_response

        self.assertEqual([company_response], companies_router.get_companies())

    def test_getCompanies_returns_emptyList_when_noData(self):
        mock_company_service.all = lambda name, location: []

        self.assertEqual([], companies_router.get_companies())

    def test_getCompanyById_returns_Company_whenFound(self):
        company = fake_company()
        company_response = CompanyResponse(id=1, name='name', info='info', location='city', contacts=None,
            active_ads_num=0, active_ads_list=[], successfull_matches=0)

        mock_company_service.get_by_id = lambda id: company
        mock_company_service.create_response_object = lambda company: company_response

        self.assertEqual(company_response, companies_router.get_company_by_id(id=1))

    def test_getCompanyById_returns_NotFound_when_noCompany(self):
        mock_company_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(companies_router.get_company_by_id(id=1)))

    def test_updateCompany_returns_updatedCompanyResponse_when_successfull(self):
        company = fake_company()
        company_response = CompanyResponse(id=1, name='comp', info='info', location='city', contacts=None,
            active_ads_num=0, active_ads_list=[], successfull_matches=0)
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: company
        mock_company_service.update = lambda old, new: company
        mock_company_service.create_response_object = lambda company: company_response

        self.assertEqual(company_response, companies_router.update_company(id=1, company=company))

    def test_updateCompany_returns_Unauthorized_when_loggedInCompany_differentFrom_targetCompany(self):
        comp1 = fake_company()
        comp2 = fake_company(id=2)
        mock_auth.return_value = comp1
        mock_company_service.get_by_id = lambda id: comp2

        self.assertEqual(Unauthorized, type(companies_router.update_company(id=2, company=comp1)))

    def test_updateCompany_returns_NotFound_when_noCompanyFound(self):
        company = fake_company()
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(companies_router.update_company(id=2, company=company)))

    def test_createCompanyContacts_returns_contactsResponseObject_when_successfull(self):
        company = fake_company()
        contacts = fake_contacts()
        contacts_response = ContactsResponse(phone_number=contacts.phone_number, email=contacts.email, website=contacts.website,
            linkedin=contacts.linkedin, facebook=contacts.facebook, twitter=contacts.twitter)
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: company
        mock_contacts_service.create = lambda contacts, table: contacts
        mock_contacts_service.create_response_object = lambda contacts: contacts_response

        self.assertEqual(contacts_response, companies_router.create_company_contacts(id=1, contacts=contacts))

    def test_createCompanyContacts_returns_Unauthorized_when_loggedInCompany_differentFrom_targetCompany(self):
        comp1 = fake_company()
        comp2 = fake_company(id=2)
        contact = fake_contacts()
        mock_auth.return_value = comp1
        mock_company_service.get_by_id = lambda id: comp2

        self.assertEqual(Unauthorized, type(companies_router.create_company_contacts(id=2, contacts=contact)))

    def test_createCompanyContacts_returns_NotFound_when_noCompanyFound(self):
        company = fake_company()
        contacts = fake_contacts()
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: None
        
        self.assertEqual(NotFound, type(companies_router.create_company_contacts(id=2, contacts=contacts)))

    def test_updateCompanyContacts_returns_updatedContactsResponseObject_when_successfull(self):
        company = fake_company()
        contacts = fake_contacts()
        contacts_response = ContactsResponse(phone_number=contacts.phone_number, email=contacts.email, website=contacts.website,
            linkedin=contacts.linkedin, facebook=contacts.facebook, twitter=contacts.twitter)
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: company
        mock_contacts_service.get_by_user_id = lambda id, table: contacts
        mock_contacts_service.update_contacts = lambda old, new, table: contacts
        mock_contacts_service.create_response_object = lambda contacts: contacts_response

        self.assertEqual(contacts_response, companies_router.update_company_contacts(id=1, contacts=contacts))

    def test_updateCompanyContacts_returns_Unauthorized_when_loggedInCompany_differentFrom_targetCompany(self):
        comp1 = fake_company()
        comp2 = fake_company(id=2)
        contacts = fake_contacts()
        mock_auth.return_value = comp1
        mock_company_service.get_by_id = lambda id: comp2
        mock_contacts_service.get_by_user_id = lambda id, table: contacts

        self.assertEqual(Unauthorized, type(companies_router.update_company_contacts(id=2, contacts=contacts)))

    def test_updateCompanyContacts_returns_NotFound_when_noCompanyFound(self):
        company = fake_company()
        contacts = fake_contacts()
        mock_auth.return_value = company
        mock_company_service.get_by_id = lambda id: None
        mock_contacts_service.get_by_user_id = lambda id, table: contacts

        self.assertEqual(NotFound, type(companies_router.update_company_contacts(id=2, contacts=contacts)))
import unittest
from unittest.mock import Mock
from services import contacts_service
from data.models import ContactsCreationData, Contacts, ContactsResponse, DBTable

class ContactsService_Should(unittest.TestCase):

    def test_getByUserId_returns_contacts_whenData(self):
        get_data_func = lambda q, a: [(1, '1111', 'email', 'website', 'linkedin', 'facebook', 'twitter', 1)]

        expected = Contacts(id=1, phone_number='1111', email='email', website='website', linkedin='linkedin',
            facebook='facebook', twitter='twitter', user_id=1)
        result = contacts_service.get_by_user_id(id=1, table=DBTable.COMPANY_CONTACTS, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByUserId_returns_None_when_noData(self):
        get_data_func = lambda q, a: []

        self.assertEqual(None, contacts_service.get_by_user_id(id=1, table=DBTable.COMPANY_CONTACTS, get_data_func=get_data_func))

    def test_updateContacts_returns_updatedContacts(self):
        con1 = Contacts(id=1, phone_number='1111', email='email1', website='website1', linkedin='linkedin1',
            facebook='facebook1', twitter='twitter1', user_id=1)
        con2 = Contacts(id=2, phone_number='2222', email='email2', website='website2', linkedin='linkedin2',
            facebook='facebook2', twitter='twitter2', user_id=2)

        update_data_func = lambda q,a: None

        expected = Contacts(id=con1.id, phone_number=con2.phone_number, email=con2.email, website=con2.website, linkedin=con2.linkedin,
            facebook=con2.facebook, twitter=con2.twitter, user_id=con1.user_id)
        result = contacts_service.update_contacts(old=con1, new=con2, table=DBTable.COMPANY_CONTACTS, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_create_returns_contacts(self):
        contacts = ContactsCreationData(phone_number='1111', email='email', user_id=1)
        insert_data_func = lambda q, a: 1
        expected = Contacts(id=1, phone_number='1111', email='email', user_id=1)
        result = contacts_service.create(contacts=contacts, table=DBTable.COMPANY_CONTACTS, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)

    def test_createResponseObject_returns_ResponseObject(self):
        contacts = Contacts(id=1, phone_number='1111', email='email', user_id=1)
        contacts_response = ContactsResponse(phone_number=contacts.phone_number, email=contacts.email)

        self.assertEqual(contacts_response, contacts_service.create_response_object(contacts=contacts))
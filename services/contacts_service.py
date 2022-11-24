from data.models import ContactsCreationData, Contacts, ContactsResponse, DBTable, UserType
from data import database

def get_by_user_id(id: int, table: str, get_data_func = None) -> ContactsResponse | None:
    if get_data_func is None:
        get_data_func = database.read_query
    
    if table == DBTable.COMPANY_CONTACTS:
        user_type = UserType.COMPANY
    else:
        user_type = UserType.PROFESSIONAL

    data = get_data_func(f'''SELECT * FROM {table} WHERE {user_type}_id = ?''', (id,))

    return next((Contacts.from_query_result(*row) for row in data), None)

def update_contacts(old: Contacts, new: Contacts, table: str, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    if table == DBTable.COMPANY_CONTACTS:
        user_type = UserType.COMPANY
    else:
        user_type = UserType.PROFESSIONAL

    merged = Contacts(
        id = old.id,
        phone_number= new.phone_number,
        email = new.email,
        website = new.website or old.website,
        linkedin = new.linkedin or old.linkedin,
        facebook = new.facebook or old.facebook,
        twitter = new.twitter or old.twitter,
        user_id = old.user_id)

    update_data_func(
        f'''UPDATE {table} SET
        phone_number = ?, email = ?, website = ?, linkedin = ?, facebook = ?, twitter = ?
        WHERE {user_type}_id = ?''',
        (merged.phone_number, merged.email, merged.website, merged.linkedin, merged.facebook, merged.twitter, merged.user_id))

    return merged

def create(contacts: ContactsCreationData, table: str, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = database.insert_query

    if table == DBTable.COMPANY_CONTACTS:
        user_type = UserType.COMPANY
    else:
        user_type = UserType.PROFESSIONAL

    generated_id = insert_data_func(
        f'''INSERT INTO {table}(phone_number, email, website, linkedin, facebook, twitter, {user_type}_id) VALUES(?,?,?,?,?,?,?)''',
        (contacts.phone_number, contacts.email, contacts.website, contacts.linkedin, contacts.facebook, contacts.twitter, contacts.user_id))

    return Contacts(
        id = generated_id,
        phone_number = contacts.phone_number,
        email = contacts.email,
        website = contacts.website,
        linkedin = contacts.linkedin,
        facebook = contacts.facebook,
        twitter = contacts.twitter,
        user_id = contacts.user_id)

def create_response_object(contacts: Contacts):
    return ContactsResponse(
        phone_number = contacts.phone_number,
        email = contacts.email,
        website = contacts.website,
        linkedin = contacts.linkedin,
        facebook = contacts.facebook,
        twitter = contacts.twitter)

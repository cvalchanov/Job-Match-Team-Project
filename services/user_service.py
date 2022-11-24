from data.models import AdminRegisterData, UserType, Company, Professional, Admin, DBTable
from mariadb import IntegrityError
from data import database
import jwt
from datetime import datetime, timedelta


SECRET = 'the sky is blue'

def hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def get_by_username(username: str, table: str, get_data_func = None) -> Company | Professional | Admin | None:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        f'''SELECT * FROM {table} WHERE username = ?''',
        (username,))

    if table == DBTable.COMPANIES:
        return next((Company.from_query_result(*row) for row in data), None)
    elif table == DBTable.PROFESSIONALS:
        return next((Professional.from_query_result(*row) for row in data), None)
    else:
        return next((Admin.from_query_result(*row) for row in data), None)        

def get_by_id(id: int, table: str, get_data_func = None) -> Company | Professional | Admin | None:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        f'''SELECT * FROM {table} WHERE id = ?''', (id,))

    if table == DBTable.COMPANIES:
        return next((Company.from_query_result(*row) for row in data), None)
    elif table == DBTable.PROFESSIONALS:
        return next((Professional.from_query_result(*row) for row in data), None)
    else:
        return next((Admin.from_query_result(*row) for row in data), None) 


def try_login(username: str, password: str, table: str) -> Company | Professional | Admin | None:
    user = get_by_username(username=username, table=table)

    password = hash_password(password)
    return user if user and user.password == password else None


def create(registration_data: AdminRegisterData, insert_data_func = None) -> Admin | None:
    if insert_data_func is None:
        insert_data_func = database.insert_query

    password = hash_password(registration_data.password)

    try:
        generated_id = insert_data_func(
            '''INSERT INTO admins(username, password) VALUES (?,?)''',
            (registration_data.username, password))

        return Admin(id= generated_id, username=registration_data.username, password='')
    except IntegrityError:
        return None

def create_token(user: Company | Professional | Admin) -> str:
    datestamp = datetime.now()
    token_expiration = datestamp + timedelta(days=14)
    if type(user) is Company:
        user_type = UserType.COMPANY
    elif type(user) is Admin:
        user_type = UserType.ADMIN
    else:
        user_type = UserType.PROFESSIONAL
    token = jwt.encode({'exp': token_expiration, 'id': user.id, 'username': user.username, "type": user_type}, SECRET, algorithm="HS256") 
    return token

def decode_token(token):
    try:
        user_info = jwt.decode(token, SECRET, algorithms=["HS256"])
        return user_info
    except jwt.PyJWTError:
        return None 


def is_authenticated(token: str, get_data_func = None) -> bool | None:
    if get_data_func is None:
        get_data_func = database.read_query

    user_info = decode_token(token=token)
    if user_info is None:
        return None
    else:
        user_id = user_info['id']
        user_username = user_info['username']
        user_type = user_info['type']
        if user_type == UserType.COMPANY:
            return any(get_data_func(
                '''SELECT 1 FROM companies where id = ? and username = ?''',
                (user_id, user_username)))
        elif user_type == UserType.PROFESSIONAL:
            return any(get_data_func(
                '''SELECT 1 FROM professionals where id = ? and username = ?''',
                (user_id, user_username)))
        else:
            return any(get_data_func(
                '''SELECT 1 FROM admins where id = ? and username = ?''',
                (user_id, user_username)))                      


def from_token(token: str) -> Company | Professional | Admin | None:
    user_info = decode_token(token=token)
    if user_info is None:
        return None
    else:
        user_username = user_info['username']
        user_type = user_info['type']
        if user_type == UserType.COMPANY:
            return get_by_username(username=user_username, table=DBTable.COMPANIES)
        elif user_type == UserType.PROFESSIONAL:
            return get_by_username(username=user_username, table=DBTable.PROFESSIONALS)
        else:
            return get_by_username(username=user_username, table=DBTable.ADMINS)       

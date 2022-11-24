from data import database
from data.models import Company, Professional, UserType, DBTable, DBColumn, MatchRequestResponse, ConfirmedMatchResponse
from services import professional_ad_service, job_ad_service, company_service, professional_service

def create(user: Company | Professional, ad_id: int, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = database.insert_query

    if type(user) is Company:
        db_table = DBTable.PROFESSIONAL_ADS_MATCH_REQUESTS
        ad_type_column = DBColumn.PROFESSIONAL_AD
        user_type_column = UserType.COMPANY
        target_user_column = UserType.PROFESSIONAL
        ad = professional_ad_service.get_professional_ad_by_ad_id(ad_id=ad_id)
        ad_response = professional_ad_service.get_professional_ad_resp_by_ad_id(id=ad_id)
        user_response = company_service.create_response_object(company=user)
        generated_id = insert_data_func(
            f'''INSERT INTO {db_table}({ad_type_column}_id, {target_user_column}_id, {user_type_column}_id) VALUES (?,?,?)''',
            (ad_id, ad.professional_id, user.id))
    else:
        db_table = DBTable.JOB_ADS_MATCH_REQUESTS
        ad_type_column = DBColumn.JOB_AD
        user_type_column = UserType.PROFESSIONAL
        target_user_column = UserType.COMPANY
        ad = list(job_ad_service.get_by_id(id=ad_id))
        ad_response = job_ad_service.create_response_object(job_ad=ad[0])
        user_response = professional_service.create_response_object(professional=user)
        generated_id = insert_data_func(
            f'''INSERT INTO {db_table}({ad_type_column}_id, {target_user_column}_id, {user_type_column}_id) VALUES (?,?,?)''',
            (ad_id, ad[0].company_id, user.id))


    return MatchRequestResponse(id=generated_id, ad=ad_response, user=user_response)

def get_by_id(id: int, user: Company | Professional, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if type(user) is Company:
        user_type = UserType.COMPANY
        db_table = DBTable.JOB_ADS_MATCH_REQUESTS
    else:
        user_type = UserType.PROFESSIONAL
        db_table = DBTable.PROFESSIONAL_ADS_MATCH_REQUESTS

    data = get_data_func(f'''SELECT * FROM {db_table} WHERE id = ?''', (id,))
    if data and user_type == UserType.COMPANY:
        ad = list(job_ad_service.get_by_id(id=data[0][1]))
        ad_response = job_ad_service.create_response_object(job_ad=ad[0])
        user = professional_service.get_by_id(id=data[0][-1])
        user_response = professional_service.create_response_object(professional=user)
    else:
        ad = professional_ad_service.get_professional_ad_by_ad_id(ad_id=data[0][1])
        ad_response = professional_ad_service.create_response_object(ad=ad, first=user.first_name, last=user.last_name)
        user = company_service.get_by_id(id=data[0][-1])
        user_response = company_service.create_response_object(company=user)

    return MatchRequestResponse(id=id, ad=ad_response, user=user_response) or None


def get_by_user(user: Company | Professional, get_data_func = None) -> list[MatchRequestResponse]:
    if get_data_func is None:
        get_data_func = database.read_query

    if type(user) is Company:
        db_table = DBTable.JOB_ADS_MATCH_REQUESTS
        user_type_column = UserType.COMPANY
    else:
        db_table = DBTable.PROFESSIONAL_ADS_MATCH_REQUESTS
        user_type_column = UserType.PROFESSIONAL

    data = get_data_func(f'''SELECT * FROM {db_table} WHERE {user_type_column}_id = ?''', (user.id,))
    ads = []
    users = []
    ids = []
    for row in data:
        if type(user) is Company:
            ad = list(job_ad_service.get_by_id(id=row[1]))
            ad_response = job_ad_service.create_response_object(job_ad=ad[0])
            pro = professional_service.get_by_id(id=row[-1])
            pro_response = professional_service.create_response_object(professional=pro)
            ads.append(ad_response)
            users.append(pro_response)
            ids.append(row[0])
        else:
            ad = professional_ad_service.get_professional_ad_by_ad_id(ad_id=row[1])
            ad_response = professional_ad_service.create_response_object(ad=ad, first=user.first_name, last=user.last_name)
            company = company_service.get_by_id(id=row[-1])
            company_response = company_service.create_response_object(company=company)
            ads.append(ad_response)
            users.append(company_response)
            ids.append(row[0])

    match_responses = []
    for x in range(len(ads)):
        match_response = MatchRequestResponse(id= ids[x], ad=ads[x], user=users[x])
        match_responses.append(match_response)

    return match_responses

def confirm(id: int, user: Company | Professional, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = database.insert_query

    mr = get_by_id(id=id, user=user)
    if type(user) is Company:
        generated_id = insert_data_func('''INSERT INTO successfull_matches(professional_id, company_id) VALUES (?,?)''', (mr.user.id, user.id))
        pro = professional_service.get_by_id(id=mr.user.id)
        pro_response = professional_service.create_response_object(professional=pro)
        company_response = company_service.create_response_object(company=user)
        match_response = ConfirmedMatchResponse(id=generated_id, professional_id=pro.id, professional_name=f'{pro.first_name} {pro.last_name}')
    else:
        generated_id = insert_data_func('''INSERT INTO successfull_matches(professional_id, company_id) VALUES (?,?)''', (user.id, mr.user.id))
        company = company_service.get_by_id(id=mr.user.id)
        company_response = company_service.create_response_object(company=company)
        pro_response = professional_service.create_response_object(professional=user)
        match_response = ConfirmedMatchResponse(id=generated_id, company_id=company.id, company_name=company.name)

    delete(pro_id=pro_response.id, comp_id=company_response.id)
    professional_service.change_status(id=pro_response.id)
    return match_response

def delete_by_id(id: int, user: Company | Professional, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    if type(user) is Company:
        db_table = DBTable.JOB_ADS_MATCH_REQUESTS
    else:
        db_table = DBTable.PROFESSIONAL_ADS_MATCH_REQUESTS
    
    update_data_func(f'''DELETE FROM {db_table} WHERE id = ?''', (id,))

def delete(pro_id: int, comp_id: int, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    update_data_func('''DELETE FROM job_ads_match_requests WHERE company_id = ? and professional_id = ?''', (comp_id, pro_id))
    update_data_func('''DELETE FROM professional_ads_match_requests WHERE company_id = ? and professional_id = ?''', (comp_id, pro_id))

def get_successfull_matches(user_id: int, user_type: str, get_data_func = None) -> list[ConfirmedMatchResponse]:
    if get_data_func is None: 
        get_data_func = database.read_query

    data = get_data_func(f'''SELECT * FROM successfull_matches WHERE {user_type}_id = ?''', (user_id,))
    successfull_matches = []

    if user_type == UserType.COMPANY:
        for row in data:
            pro = professional_service.get_by_id(id=row[1])
            response = ConfirmedMatchResponse(id=row[0], professional_id=pro.id, professional_name=f'{pro.first_name + pro.last_name}')
            successfull_matches.append(response)
    else:
        for row in data:
            company = company_service.get_by_id(id=row[1])
            response = ConfirmedMatchResponse(id=row[0], company_id=company.id, company_name=company.name)
            successfull_matches.append(response)

    return successfull_matches

def check_if_owner(user: Company | Professional, mr_id: int):
    match_requests = get_by_user(user=user)
    return mr_id in [mr.id for mr in match_requests]

from data.models import Company, Professional, SearchResultSkillsetResponse, SearchResultSkillResponse
from data.models import SearchResponse, SearchResult, UserType, DBTable, DBColumn, Location, ContactsResponse
from data import database

def search(user: Company | Professional, salary_threshold: str | None = None, skillset_threshold: str | None = None):

    user_data = _get_data(user=user)
    search_results = _get_data(user=user, data=user_data, salary_threshold=salary_threshold)
    user_data_responses = create_response_objects(search_results=user_data)
    search_results_responses = create_response_objects(search_results=search_results)
    filtered_data = _filter_data(user_data_responses=user_data_responses,
                                search_results_responses=search_results_responses,
                                skillset_threshold=skillset_threshold)
    flattened_filtered_data = _flatten_data(data=filtered_data)

    return flattened_filtered_data

def _flatten_data(data: list[SearchResponse]):
    ad_ids = []
    flattened_data = []
    for sr in data:
        if sr.ad_id not in ad_ids:
            ad_ids.append(sr.ad_id)
            flattened_data.append(sr)

    return sorted(flattened_data)

def _filter_data(user_data_responses: list[SearchResponse], search_results_responses: list[SearchResponse], skillset_threshold: str):
    if not user_data_responses:
        return search_results_responses

    result = []
    if skillset_threshold:
        for udr in user_data_responses:
            for srr in search_results_responses:
                if udr.skillset == srr.skillset:
                    result.append(srr)
                else:
                    if len(udr.skillset) != 0 and len(srr.skillset) != 0:
                        differences = _compare_skillsets(user_skillset=udr.skillset, search_skillset=srr.skillset)
                        if differences <= int(skillset_threshold):
                            result.append(srr)
    else:
        for udr in user_data_responses:
            for srr in search_results_responses:
                if udr.skillset == srr.skillset:
                    result.append(srr)

    return result

def _compare_skillsets(user_skillset: list[SearchResultSkillsetResponse], search_skillset: list[SearchResultSkillsetResponse]):
    user_skillsets: list[SearchResultSkillResponse] = []
    search_skillsets = []

    for us in user_skillset:
        for uss in us.skills_in_category:
            if uss not in user_skillsets:
                user_skillsets.append(uss)
    
    for ss in search_skillset:
        for sss in ss.skills_in_category:
            if sss not in search_skillsets:
                search_skillsets.append(sss)

    if len(user_skillsets) > len(search_skillsets):
        differences = (len(user_skillsets) - len(search_skillsets))
    else:
        differences = (len(search_skillsets) - len(user_skillsets))

    for us1 in user_skillsets:
        if us1 not in search_skillsets:
            differences = differences + 1


    return differences

def create_response_objects(search_results: list[SearchResult]) -> list[SearchResponse]:
    ad_ids = []
    search_responses = []
    skills_data = {}
    skillset_responses = {}
    for sr in search_results:
        search_response = SearchResponse(ad_id=sr.ad_id, min_salary=sr.min_salary, max_salary=sr.max_salary, description=sr.description,
            remote=sr.remote, location=(Location(id=sr.city_id, name=sr.city_name) if sr.city_id else None), ad_owner_id=sr.owner_id,
            ad_owner_name=sr.owner_name, ad_owner_info=sr.owner_info, ad_owner_contacts=(ContactsResponse(phone_number=sr.phone_number,
            email=sr.email, website=sr.website, linkedin=sr.linkedin, facebook=sr.facebook, twitter=sr.twitter)) if sr.phone_number else None)
        if sr.ad_id not in ad_ids:
            search_responses.append(search_response)
            ad_ids.append(sr.ad_id)
        if sr.ad_id not in skills_data.keys():
            skills_data[sr.ad_id] = {(sr.skill_category_name, sr.skill_category_id): 
                [SearchResultSkillResponse(skill_name=sr.skill_name, skill_level_name=sr.skill_level_name)]}
        else:
            if (sr.skill_category_name, sr.skill_category_id) not in skills_data[sr.ad_id].keys():
                skills_data[sr.ad_id][sr.skill_category_name, sr.skill_category_id] = [(SearchResultSkillResponse(
                    skill_name=sr.skill_name, skill_level_name=sr.skill_level_name))]
            else:
                skills_data[sr.ad_id][sr.skill_category_name, sr.skill_category_id].append(SearchResultSkillResponse(
                    skill_name=sr.skill_name, skill_level_name=sr.skill_level_name))

    for key in skills_data:
        skillset_responses[key] = []
        for keykey in skills_data[key]:
            if keykey[1] is not None:
                skillset_response = SearchResultSkillsetResponse(category_id=keykey[1], category_name=keykey[0],
                    skills_in_category=skills_data[key][keykey])
                skillset_responses[key].append(skillset_response)

    for s in search_responses:
        s.skillset = s.skillset + skillset_responses[s.ad_id]

    return search_responses

def _get_data(user: Company | Professional, data: list[SearchResult] | None = None, salary_threshold: str | None = None, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if data is None:
        search_query = _construct_query(search_for=0, user=user)
    elif len(data) == 0:
        search_query = _construct_query(search_for=1, user=user)
    else:
        search_query = _construct_query(search_for=2, user=user, data=data, salary_threshold=salary_threshold)

    result_data = get_data_func(search_query)

    search_results = [SearchResult.from_query_result(*row) for row in result_data]

    return search_results

def _construct_query(search_for: int, user: Company | Professional, data: list[SearchResult] | None = None, salary_threshold: str | None = None):
    if search_for == 0:
        if type(user) is Company:
            user_type = UserType.COMPANY
        else:
            user_type = UserType.PROFESSIONAL
        user_table, ad_table, ad_column, ad_skillsets_table, ad_state_column, contacts_table, name_column = _set_database_tables_and_columns(user_type)    
        where_clause = f'WHERE ADS.{user_type}_id = {user.id} AND ADS.{ad_state_column} = 1'
    elif search_for == 1:
        if type(user) is Company:
            user_type = UserType.PROFESSIONAL
        else:
            user_type = UserType.COMPANY
        user_table, ad_table, ad_column, ad_skillsets_table, ad_state_column, contacts_table, name_column = _set_database_tables_and_columns(user_type)
        where_clause = f'WHERE ADS.city_id = {user.city_id} AND ADS.{ad_state_column} = 1'
    else:
        if type(user) is Company:
            user_type = UserType.PROFESSIONAL
        else:
            user_type = UserType.COMPANY
        user_table, ad_table, ad_column, ad_skillsets_table, ad_state_column, contacts_table, name_column = _set_database_tables_and_columns(user_type)
        where_clause = 'WHERE '
        remote = set(r.remote for r in data)
        location = set(r.city_id for r in data)
        min_salary_set = set(r.min_salary for r in data)
        max_salary_set = set(r.max_salary for r in data)
        if len(remote) == 1:
            where_clause = where_clause + f'ADS.remote = {list(remote)[0]} '

        if len(tuple(x for x in location if x is not None)) == 1 and None not in location and len(remote) == 1:
            where_clause = where_clause + f'AND ADS.city_id = {list(location)[0]} '
        elif len(tuple(x for x in location if x is not None)) == 1 and None not in location and len(remote) != 1:
            where_clause = where_clause + f'ADS.city_id = {list(location)[0]} '
        elif len(tuple(x for x in location if x is not None)) == 1 and None in location and len(remote) == 1:
            where_clause = where_clause + f'AND (ADS.city_id = {list(x for x in location if x is not None)[0]} OR ADS.city_id is null) '
        elif len(tuple(x for x in location if x is not None)) == 1 and None in location and len(remote) != 1:
            where_clause = where_clause + f'(ADS.city_id = {list(x for x in location if x is not None)[0]} OR ADS.city_id is null) '
        elif len(tuple(x for x in location if x is not None)) > 1 and None not in location and len(remote) == 1:
            where_clause = where_clause + f'AND ADS.city_id IN {tuple(x for x in location if x is not None)} '
        elif len(tuple(x for x in location if x is not None)) > 1 and None not in location and len(remote) != 1:
            where_clause = where_clause + f'ADS.city_id IN {tuple(x for x in location if x is not None)} '
        elif len(tuple(x for x in location if x is not None)) > 1 and None in location and len(remote) == 1:
            where_clause = where_clause + f'AND (ADS.city_id IN {tuple(x for x in location if x is not None)} OR ADS.city_id is null) '
        elif len(tuple(x for x in location if x is not None)) > 1 and None in location and len(remote) != 1:
            where_clause = where_clause + f'(ADS.city_id IN {tuple(x for x in location if x is not None)} OR ADS.city_id is null) '
        elif len(tuple(x for x in location if x is not None)) == 0 and len(remote) == 1:
            where_clause = where_clause + f'AND ADS.city_id is null '
        elif len(tuple(x for x in location if x is not None)) == 0 and len(remote) != 1:
            where_clause = where_clause + f'ADS.city_id is null '

        min_salary_bot = min(min_salary_set)
        min_salary_top = max(min_salary_set)
        max_salary_bot = min(max_salary_set)
        max_salary_top = max(max_salary_set)

        if salary_threshold:
            min_salary_bot = min_salary_bot - min_salary_bot*(int(salary_threshold)/100)
            min_salary_top = min_salary_top + min_salary_top*(int(salary_threshold)/100)
            max_salary_bot = max_salary_bot - max_salary_bot*(int(salary_threshold)/100)
            max_salary_top = max_salary_top + max_salary_top*(int(salary_threshold)/100)
        
        where_clause = (where_clause + 
            f'AND (ADS.min_salary BETWEEN {min_salary_bot} AND {min_salary_top}) AND (ADS.max_salary BETWEEN {max_salary_bot} and {max_salary_top}) ')
        where_clause = where_clause + f'AND ADS.{ad_state_column} = 1'
    search_query = f'''SELECT ADS.id, ADS.min_salary, ADS.max_salary, ADS.description, ADS.remote, ADS.city_id, cities.name,
    ADSS.skill_id, skills.name, ADSS.skill_level_id, skill_levels.level_name, skill_categories.id, skill_categories.name,
    O.id, {name_column}, O.info, C.id, C.phone_number, C.email, C.website, C.linkedin, C.facebook, C.twitter
    FROM {ad_table} AS ADS
    LEFT JOIN cities ON cities.id = ADS.city_id
    LEFT JOIN {ad_skillsets_table} AS ADSS ON ADS.id = ADSS.{ad_column}_id
    LEFT JOIN skills ON skills.id = ADSS.skill_id
    LEFT JOIN skill_levels ON skill_levels.id = ADSS.skill_level_id
    LEFT JOIN skill_categories ON skill_categories.id = skills.skill_category_id
    LEFT JOIN {contacts_table} AS C ON ADS.{user_type}_id = C.{user_type}_id
    JOIN {user_table} AS O ON O.id = ADS.{user_type}_id
    {where_clause}'''

    return search_query

def _set_database_tables_and_columns(user_type: str):
    if user_type == UserType.COMPANY:
        user_table = DBTable.COMPANIES
        ad_table = DBTable.JOB_ADS
        ad_column = DBColumn.JOB_AD
        ad_skillsets_table = DBTable.JOB_ADS_SKILLSETS
        ad_state_column = DBColumn.JOB_AD_STATE_COLUMN
        contacts_table = DBTable.COMPANY_CONTACTS
        name_column = DBColumn.COMPANY_NAME_COLUMN_FOR_SEARCH
    else:
        user_table = DBTable.PROFESSIONALS
        ad_table = DBTable.PROFESSIONAL_ADS
        ad_column = DBColumn.PROFESSIONAL_AD
        ad_skillsets_table = DBTable.PROFESSIONAL_ADS_SKILLSETS
        ad_state_column = DBColumn.PROFESSIONAL_AD_STATE_COLUMN
        contacts_table = DBTable.PROFESSIONAL_CONTACTS
        name_column = DBColumn.PROFESSIONAL_NAME_COLUMN_FOR_SEARCH

    return [user_table, ad_table, ad_column, ad_skillsets_table, ad_state_column, contacts_table, name_column]
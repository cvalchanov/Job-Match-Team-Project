from data.database import insert_query, read_query, update_query
from data.models import ProfessionalAd, ProfessionalAdResponse, Skillset, DBColumn, DBTable
from services import skill_service, location_service, ad_state_service

def get_all_professional_ads_resps_by_status(status: str, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''SELECT ads.id, ads.min_salary, ads.max_salary, ads.description, ads.remote, st.name, c.name, p.first_name, p.last_name
            FROM professional_ads AS ads
            JOIN professionals AS p ON ads.professional_id = p.id
            JOIN ad_states AS st ON ads.ad_state_id = st.id
            LEFT JOIN cities AS c ON ads.city_id = c.id 
            WHERE st.name = ?''', (status,))
    
    ads = _get_prof_ads(data)
    return ads

def get_professional_ads_resps_by_user(user_id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''SELECT ads.id, ads.min_salary, ads.max_salary, ads.description, ads.remote, st.name, c.name, p.first_name, p.last_name
            FROM professional_ads AS ads
            JOIN professionals AS p ON ads.professional_id = p.id
            JOIN ad_states AS st ON ads.ad_state_id = st.id
            LEFT JOIN cities AS c ON ads.city_id = c.id 
            WHERE professional_id.id = ?''', (user_id,))
    
    ads = _get_prof_ads(data)
    return ads

def get_professional_ad_by_ad_id(ad_id: int, get_data_func = None) -> ProfessionalAd:
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''SELECT *
            FROM professional_ads
            WHERE id = ?''', (ad_id,))
    
    return next((ProfessionalAd.from_query_result(*row) for row in data), None)

def get_professional_id_by_ad_id(ad_id: int, get_data_func = None) -> int:
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''select professional_id from professional_ads where id = ?''', (ad_id,))
    
    return data[0][0]


def get_professional_ad_resp_by_ad_id(id: int, get_data_func = None) -> ProfessionalAdResponse | None:
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''SELECT ads.id, ads.min_salary, ads.max_salary, ads.description, ads.remote, st.name, c.name, p.first_name, p.last_name
            FROM professional_ads AS ads
            JOIN professionals AS p ON ads.professional_id = p.id
            JOIN ad_states AS st ON ads.ad_state_id = st.id
            LEFT JOIN cities AS c ON ads.city_id = c.id 
            WHERE ads.id = ?''', (id,))

    ads = _get_prof_ads(data)
    if ads:
        return ads[0]
    return None
    # return next((ProfessionalAd.from_query_result(*row, professional_first_name = user_first_name, professional_last_name = user_last_name) for row in data), None)

def create_professional_ad(prof_ad: ProfessionalAd, skillset: list[Skillset], insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query

    generated_id = insert_data_func(
        'INSERT INTO professional_ads(min_salary, max_salary, description, remote, professional_id, city_id, ad_state_id) VALUES(?,?,?,?,?,?,?)',
        (prof_ad.min_salary, prof_ad.max_salary, prof_ad.description, prof_ad.remote, prof_ad.professional_id, prof_ad.city_id, prof_ad.ad_state_id))
    
    if len(skillset) == 1:
        skill_service.add_skill_to_ad(skillset[0], generated_id, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)
    elif len(skillset) > 1:
        skill_service.add_many_skills_to_ad(skillset, generated_id, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)
    prof_ad.id = generated_id

    return prof_ad

def update_profesional_ad(old: ProfessionalAd, new: ProfessionalAd, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query

    merged = ProfessionalAd(
        id= old.id,
        min_salary=new.min_salary or old.min_salary,
        max_salary=new.max_salary or old.max_salary,
        description=new.description or old.description,
        remote=new.remote or old.remote,
        professional_id=new.professional_id or old.professional_id,
        city_id=new.city_id or old.city_id,
        ad_state_id = new.ad_state_id or old.ad_state_id
    )

    update_data_func( 
        '''UPDATE professional_ads SET
           min_salary = ?, max_salary = ?, description = ?, remote = ?, professional_id = ?, city_id = ?, ad_state_id = ?
           WHERE id = ? ''',
        (merged.min_salary, merged.max_salary, merged.description, merged.remote, merged.professional_id, merged.city_id, merged.id, merged.ad_state_id))

    return merged

def delete_professional_ad(id: int, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query

    update_data_func('DELETE FROM professional_ads_skillsets WHERE professional_ad_id = ?', (id,))
    return bool(update_data_func('DELETE FROM professional_ads WHERE id = ?', (id,)))

def get_active_ads_resps_by_user(user_id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query

    status = 'active'
    data = get_data_func(
        '''SELECT professional_ads.id, professional_ads.min_salary, professional_ads.max_salary, professional_ads.description,
           professional_ads.remote, ad_states.name, cities.name, professionals.first_name, professionals.last_name 
           FROM professional_ads
           JOIN ad_states ON ad_states.id = professional_ads.ad_state_id
           LEFT JOIN cities ON cities.id = professional_ads.city_id 
           JOIN professionals ON professionals.id = professional_ads.professional_id
           WHERE ad_states.name = ? AND professional_ads.professional_id = ?''', (status, user_id))
    
    ads = _get_prof_ads(data)
    return ads

def _get_prof_ads(data) -> list[ProfessionalAdResponse]:
    ads = []
    for row in range(len(data)):
        ad = ProfessionalAdResponse.from_query_result(*data[row])
        ad.skillset.append(skill_service.get_skillset_by_ad_id(ad.id, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID))
        ads.append(ad)

    return ads
    # return (ProfessionalAdResponse.from_query_result(*row, professional_first_name = user_first_name, professional_last_name = user_last_name) for row in data)

def create_response_object(ad: ProfessionalAd, first, last) -> ProfessionalAdResponse:

    def location_string(id: int):
        location = location_service.get_location_by_id(id) 
        return location.name

    def remote_string(remote: bool):
        if remote == True:
            return 'Yes'
        else:
            return 'No'
            
    def status_string(status: int):
        state = ad_state_service.get_ad_state_by_id(status)
        return state.name
    
    return ProfessionalAdResponse(
            id = ad.id,
            min_salary = ad.min_salary,
            max_salary = ad.max_salary,
            description = ad.description,
            remote = remote_string(ad.remote),
            status = status_string(ad.ad_state_id),
            city_name = location_string(ad.city_id),
            professional_first_name = first,
            professional_last_name = last,
            skillset = skill_service.get_skillset_by_ad_id(ad.id, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)
        )
def is_creator(ad_id: int, user_id):
    ad = read_query(
        ''' SELECT professional_id
            FROM professional_ads
            WHERE professional_id = ? AND id = ?''', (user_id, ad_id))
    
    if ad:
        return True
    
    return False
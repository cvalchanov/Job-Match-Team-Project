from data.database import insert_query, read_query, update_query
from data.models import JobAd, JobAdResponse, Company, Admin, Professional
from common.responses import NotFound
from services import company_service, location_service, skill_service


def all(get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
        data = get_data_func('''select * from job_ads''')

        if data is None:
            return NotFound()
        else:
            return (JobAd.from_query_result(*row) for row in data)


def all_by_company(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
        data = get_data_func('''select * from job_ads where company_id = ?''',(id,))
    return (JobAd.from_query_result(*row) for row in data)


def all_archived(get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
    data = get_data_func('''select * from job_ads where status = false''')
    return (JobAd.from_query_result(*row) for row in data)


def all_active(get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
    data = get_data_func('''select * from job_ads where status = true''')
    return (JobAd.from_query_result(*row) for row in data)


def all_archived_by_company_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
    data = get_data_func('''select * from job_ads where status = false and company_id = ?''',(id,))

    return (JobAd.from_query_result(*row) for row in data)


def all_active_by_company_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
    data = get_data_func('''select * from job_ads where status = true and company_id = ?''',(id,))
    return (JobAd.from_query_result(*row) for row in data)


def get_by_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = read_query
        data = get_data_func('''select * from job_ads where id = ?''', (id,))

    return (JobAd.from_query_result(*row) for row in data)

def get_company_id_by_ad_id(ad_id: int, get_data_func = None) -> int:
    if get_data_func is None:
        get_data_func = read_query

    data = get_data_func(
        '''select company_id from job_ads where id = ?''', (ad_id,))
    
    return data[0][0]


def create(job_ad: JobAd, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = insert_query
    generated_id = insert_data_func('''insert into job_ads(min_salary, max_salary, description, remote, status, company_id, city_id) values (?,?,?,?,?,?,?)''',
    (job_ad.min_salary, job_ad.max_salary, job_ad.description, job_ad.remote, job_ad.status, job_ad.company_id, job_ad.city_id))
    job_ad.id = generated_id
    return job_ad


def update(old: JobAd, new: JobAd, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query

        merged = JobAd(
            id = old.id,
            min_salary = new.min_salary or old.min_salary,
            max_salary = new.max_salary or old.max_salary,
            description = new.description or old.description,
            remote = new.remote,
            status = new.status,
            company_id = old.company_id,
            city_id = new.city_id or old.city_id)


        update_data_func('''update job_ads set min_salary = ?, max_salary = ?, description = ?, remote = ?, status = ?, company_id = ?, city_id = ? where id = ?''',
        (merged.min_salary, merged.max_salary, merged.description, merged.remote, merged.status, merged.company_id, merged.city_id, merged.id))
        return merged
  

def delete(id: int): 
    update_query('delete from job_ads where id = ?', (id,))



def create_response_object(job_ad: JobAd) -> JobAdResponse:

    def company_string(id: int):
        comp = company_service.get_by_id(id)
        return comp.name

    def location_string(id: int):
        location = location_service.get_location_by_id(id) 
        return location.name

    def remote_string(remote: bool):
        if remote == True:
            return 'Yes'
        else:
            return 'No'
            
    def status_string(status: bool):
        if status == True:
            return 'Active'
        else:
            return 'Archived'

    if job_ad.city_id:
        location = location_string(job_ad.city_id)
    else:
        location = None
    
    return JobAdResponse(
        id = job_ad.id,
        min_salary = job_ad.min_salary,
        max_salary = job_ad.max_salary,
        description = job_ad.description,
        remote = remote_string(job_ad.remote),
        status = status_string(job_ad.status),
        company = company_string(job_ad.company_id),
        location = location,
        skill_set = skill_service.get_skillset_by_ad_id(job_ad.id, 'job_ads_skillsets', 'job_ad_id'))


def is_company(user) -> bool:
    x = isinstance(user, Company)
    return x

def is_admin(user) -> bool:
    x = isinstance(user, Admin)
    return x

def is_professional(user) -> bool:
    x = isinstance(user, Professional)
    return x

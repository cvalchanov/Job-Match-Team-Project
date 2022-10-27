from data.database import insert_query, read_query, update_query
from data.models import ProfessionalAd


def get_professional_ads_all():
    data = read_query(
    '''SELECT *
        FROM professional_ads''')

    return (ProfessionalAd.from_query_result(*row) for row in data)


def get_professional_ad_by_id(id: int):
    data = read_query(
        '''SELECT *
            FROM professional_ads 
            WHERE id = ?''', (id,))

    return next((ProfessionalAd.from_query_result(*row) for row in data), None)

def create_professional_ad(company_ad: ProfessionalAd):
    generated_id = insert_query(
        'INSERT INTO professional_ads(min_salary, max_salary, description, remote, status, professional_id, city_id) VALUES(?,?,?,?,?,?,?)',
        (company_ad.min_salary, company_ad.max_salary, company_ad.description, company_ad.remote, company_ad.status, company_ad.professional_id, company_ad.city_id))

    company_ad.id = generated_id

    return company_ad

def update_profesional_ad(old: ProfessionalAd, new: ProfessionalAd):
    merged = ProfessionalAd(
        id= old.id,
        min_salary=new.min_salary or old.min_salary,
        max_salary=new.max_salary or old.max_salary,
        description=new.description or old.description,
        remote=new.remote or old.remote,
        status=new.status or old.status,
        professional_id=new.professional_id or old.professional_id,
        city_id=new.city_id or old.city_id
    )

    update_query( 
        '''UPDATE professional_ads SET
           min_salary = ?, max_salary = ?, description = ?, remote = ?, status = ?, professional_id = ?, city_id = ?
           WHERE id = ? ''',
        (merged.min_salary, merged.max_salary, merged.description, merged.remote, merged.status, merged.professional_id, merged.city_id, merged.id))

    return merged

def delete_professional_ad(id: int):
    update_query('delete from professional_ads where id = ?', (id,))

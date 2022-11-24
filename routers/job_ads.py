from fastapi import APIRouter, Header
from services import job_ad_service
from data.models import JobAd
from common.auth import get_user_or_raise_401
from common.responses import NoContent, Unauthorized, NotFound
from services.mailjet_service import mailjet
from services import mailjet_service, company_service


job_ads_router = APIRouter(prefix = '/job_ads')


    

@job_ads_router.get('/')
def get_job_ads(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        job_ads = job_ad_service.all()
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]

    elif job_ad_service.is_company(user):
        job_ads = job_ad_service.all_by_company(user.id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]

    else:
        return Unauthorized()
        
# if authenticated company - gets all job ads of the current company
# if authenticated admin - gets all job ads


@job_ads_router.get('/active')
def get_job_ads(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        job_ads = job_ad_service.all_active()
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]
    
    if job_ad_service.is_company(user):
        job_ads = job_ad_service.all_active_by_company_id(user.id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]
        
# if authenticated company - gets all active job ads of the current company
# if authenticated admin - gets all active job ads



@job_ads_router.get('/archived')
def get_job_ads(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        job_ads = job_ad_service.all_archived()
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]

    if job_ad_service.is_company(user):
        job_ads = job_ad_service.all_archived_by_company_id(user.id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            return [job_ad_service.create_response_object(job_ad) for job_ad in job_ads_list]

# if authenticated company - gets all archived job ads of the current company
# if authenticated admin - gets all archived job ads



@job_ads_router.get('/{id}')
def get_job_ad_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        job_ads = job_ad_service.get_by_id(id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NotFound()

        else:
            job_ad = job_ads_list[0]
            return job_ad_service.create_response_object(job_ad)

    if job_ad_service.is_company(user):
        job_ads = job_ad_service.get_by_id(id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NotFound()

        else:
            job_ad = job_ads_list[0]

            if job_ad.company_id == user.id:
                return job_ad_service.create_response_object(job_ad)

            else:
                return Unauthorized()

# if authenticated admin - gets a job ad by id
# if authenticated company - gets a job by id but only if it's an ad of the current company


@job_ads_router.post('/')
def create_job_ad(job_ad: JobAd, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    if job_ad_service.is_admin(user):
        job_ad_service.create(job_ad)
        return job_ad_service.create_response_object(job_ad)
    
    elif job_ad_service.is_company(user):


        if job_ad.company_id is None:
            job_ad.company_id = user.id
            job_ad_service.create(job_ad)
            company_email = company_service.get_company_email_by_id(user.id)
            data = mailjet_service.create_email_for_creation_of_ad(company_email, user.name)
            mailjet.send.create(data)
            return job_ad_service.create_response_object(job_ad)

        if job_ad.company_id and job_ad.company_id != user.id:
            return Unauthorized()

        else:

            company_email = company_service.get_company_email_by_id(user.id)
            data = mailjet_service.create_email_for_creation_of_ad(company_email, user.name)
            mailjet.send.create(data)
            job_ad_service.create(job_ad)
            return job_ad_service.create_response_object(job_ad)

        
    else:
        return Unauthorized()

# if authenticated company or admin - creates a new job ad
# for admins company_id is required, for companies it is not, as it is the same as the id of the authenticated company
# an email notification is sent to the company's email when successful creation of ad
# example body for admins:

# {"min_salary":1000,
# "max_salary":2500,
# "description":"new job",
# "remote":0,
# "status":1,
# "company_id":1,
# "city_id":908}

# example body for companies: 

# {"min_salary":1000,
# "max_salary":2500,
# "description":"new job",
# "remote":0,
# "status":1,
# "city_id":908}
    
@job_ads_router.patch('/{id}')


        

@job_ads_router.put('/{id}')
def update_job_ad(id: int, new_job_ad: JobAd, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        old_job_ad_gen = job_ad_service.get_by_id(id)
        old_job_ad_list = list(old_job_ad_gen)

        if len(old_job_ad_list) == 0:
            return NotFound()
        
        else:
            old_job_ad = old_job_ad_list[0]
            updated_job_ad = job_ad_service.update(old_job_ad, new_job_ad)

            return job_ad_service.create_response_object(updated_job_ad)

    if job_ad_service.is_company(user):
        old_job_ad_gen = job_ad_service.get_by_id(id)
        old_job_ad_list = list(old_job_ad_gen)

        if len(old_job_ad_list) == 0:
            return NotFound()
        
        else:
            old_job_ad = old_job_ad_list[0]

            if old_job_ad.company_id == user.id: 

                updated_job_ad = job_ad_service.update(old_job_ad, new_job_ad)
                company_email = company_service.get_company_email_by_id(user.id)
                data = mailjet_service.create_email_for_update_of_ad(company_email, user.name)
                mailjet.send.create(data)
                return job_ad_service.create_response_object(updated_job_ad)

            else:
                return Unauthorized()


    
# if authenticated admin or company, updates a company by id; companies can update only their ads, otherwise -> Unauthorized
# an email notification is sent to the company's email when successful update of ad
# example body:

# {"min_salary":1200,
# "max_salary":24500,
# "description":"updated by comp22",
# "remote":1,
# "status":1,
# "city_id":920} 




        

@job_ads_router.delete('/{id}')
def delete_job_ad_by_id(id, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_admin(user):
        job_ads = job_ad_service.get_by_id(id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            job_ad = job_ads_list[0]
            job_ad_service.delete(job_ad.id) 
            return NotFound()

    if job_ad_service.is_company(user):
        job_ads = job_ad_service.get_by_id(id)
        job_ads_list = list(job_ads)

        if len(job_ads_list) == 0:
            return NoContent()

        else:
            job_ad = job_ads_list[0]

            if job_ad.company_id == user.id:
                company_email = company_service.get_company_email_by_id(user.id)
                data = mailjet_service.create_email_for_deleting_ad(company_email, user.name)
                mailjet.send.create(data)
                job_ad_service.delete(job_ad.id)
                return NotFound()
            
            else:
                return Unauthorized()
    else: 
        return Unauthorized()



# if authenticated admin - deletes a job ad by id
# if authenticated company - deletes a job ad by id but only if it's an ad of the current company
# an email notification is sent to the company's email when successful deletion of ad


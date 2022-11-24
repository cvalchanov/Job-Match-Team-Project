from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from services import match_service
from data.models import MatchRequestResponse
from common.responses import Unauthorized, NotFound, BadRequest
from services import company_service, professional_ad_service, professional_service, mailjet_service, job_ad_service
from services.mailjet_service import mailjet




match_router = APIRouter(prefix='/match')

@match_router.post('/{id}')
def create_match_request(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if job_ad_service.is_company(user):

        id_of_owner_of_ad = professional_ad_service.get_professional_id_by_ad_id(id)
        professional_email = professional_service.get_professional_email_by_id(id_of_owner_of_ad)
        data = mailjet_service.create_email_for_a_match_request(professional_email, user.name)
        mailjet.send.create(data)

        return match_service.create(user=user, ad_id=id)
    
    elif job_ad_service.is_professional(user):

        id_of_owner_of_ad = job_ad_service.get_company_id_by_ad_id(id)
        company_email = company_service.get_company_email_by_id(id_of_owner_of_ad)
        data = mailjet_service.create_email_for_a_match_request(company_email, user.first_name)
        mailjet.send.create(data)

        return match_service.create(user=user, ad_id = id)


    

@match_router.get('/', response_model=list[MatchRequestResponse])
def get_match_request(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return match_service.get_by_user(user=user)

@match_router.get('/{id}')
def get_match_request_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if user and match_service.check_if_owner(user=user, mr_id=id):
        return match_service.get_by_id(id=id, user=user) or NotFound
    elif (user and not match_service.check_if_owner(user=user, mr_id=id)) or not user:
        return Unauthorized()
    else:
        return BadRequest()

@match_router.post('/confirm/{id}')
def confirm(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    mr = match_service.get_by_id(id=id, user=user)

    if user and match_service.check_if_owner(user=user, mr_id=id):
        
        if job_ad_service.is_company(user):

            id_of_owner_of_ad = professional_ad_service.get_professional_id_by_ad_id(mr.ad.id)
            professional_email = professional_service.get_professional_email_by_id(id_of_owner_of_ad)
            data = mailjet_service.create_email_for_a_match_confirmation(professional_email, user.name)
            mailjet.send.create(data)

            return match_service.confirm(id=id, user=user)


        elif job_ad_service.is_professional(user):

            id_of_owner_of_ad = job_ad_service.get_company_id_by_ad_id(mr.ad.id)
            company_email = company_service.get_company_email_by_id(id_of_owner_of_ad)
            data = mailjet_service.create_email_for_a_match_confirmation(company_email, user.first_name)
            mailjet.send.create(data)

            return match_service.confirm(id=id, user=user)

    elif (user and not match_service.check_if_owner(user=user, mr_id=id)) or not user:
        return Unauthorized()
    else:
        return BadRequest()

@match_router.delete('/{id}')
def delete(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    if user and match_service.check_if_owner(user=user, mr_id=id):
        return match_service.delete_by_id(id=id, user=user)
    elif (user and not match_service.check_if_owner(user=user, mr_id=id)) or not user:
        return Unauthorized()
    else:
        return BadRequest()
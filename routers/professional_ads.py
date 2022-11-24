from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import NotFound, Unauthorized, BadRequest
from data.models import DBColumn, DBTable, ProfessionalAd, Skillset, Admin, Professional, DBAdStates
from services import professional_ad_service, professional_service, mailjet_service, skill_service
from services.mailjet_service import mailjet


professional_ads_router = APIRouter(prefix='/professionalads')
my_professional_ads_router = APIRouter(prefix='/myprofessionalads')

@professional_ads_router.get('/')
def get_all_professional_ads(x_token: str = Header()):
    get_user_or_raise_401(x_token)

#  Status
# · Active – the ad is visible in searches
# · Hidden – the ad is not visible for anyone but the creator
# · Private – the ad can be viewed by id, but do not appear in searches should
# · Matched – when is matched by a company

    ads = professional_ad_service.get_all_professional_ads_resps_by_status(DBAdStates.ACTIVE)

    return ads

@professional_ads_router.get('/{ad_id}')
def get_professional_ad_by_id(ad_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    # if status is active or private
    result = professional_ad_service.get_professional_ad_resp_by_ad_id(ad_id)
    if result is None:
        return NotFound()
    if result.status == DBAdStates.HIDDEN and not professional_ad_service.is_creator(ad_id, user.id):
        return Unauthorized()
    return result

@professional_ads_router.put('/{ad_id}')
def admin_update_professional_ad_by_id(ad_id: int, new_ad: ProfessionalAd, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Admin):
        return Unauthorized()

    result = professional_ad_service.get_professional_ad_resp_by_ad_id(ad_id)
    if result is None:
        return NotFound(content=f'No ad with ID {ad_id} was found')
    
    return professional_ad_service.update_profesional_ad(result, new_ad)

@professional_ads_router.delete('/{ad_id}')
def delete_my_professional_ad(ad_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Admin):
        return Unauthorized()  

    return professional_ad_service.delete_professional_ad(ad_id)

@my_professional_ads_router.get('/')
def get_my_professional_ads(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized()

    ads = professional_ad_service.get_professional_ads_resps_by_user(user.id)

    return ads

@my_professional_ads_router.post('/', status_code=201)
def create_professional_ad(prof_ad: ProfessionalAd, skillset: list[Skillset] = [], x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized()
    
    prof_ad.professional_id = user.id
    ad = professional_ad_service.create_professional_ad(prof_ad, skillset)
    professional_email = professional_service.get_professional_email_by_id(user.id)
    data = mailjet_service.create_email_for_creation_of_ad(professional_email, user.name)
    mailjet.send.create(data)
    
    return professional_ad_service.create_response_object(ad, user.first_name, user.last_name)

@my_professional_ads_router.put('/{ad_id}')
def update_my_professional_ad_by_id(ad_id: int, new_ad: ProfessionalAd, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized()

    result = professional_ad_service.get_professional_ad_by_ad_id(ad_id)
    if result is None:
        return NotFound()
    if result.professional_id != user.id:
        # return BadRequest()
        return Unauthorized()
    new_ad.professional_id = user.id

    ad = professional_ad_service.update_profesional_ad(result, new_ad)
    professional_email = professional_service.get_professional_email_by_id(user.id)
    data = mailjet_service.create_email_for_update_of_ad(professional_email, user.name)
    mailjet.send.create(data)

    return professional_ad_service.create_response_object(ad, user.first_name, user.last_name)

@my_professional_ads_router.delete('/{ad_id}')
def delete_my_professional_ad(ad_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized() 
    result = professional_ad_service.get_professional_ad_by_ad_id(ad_id)
    if result is None:
        return NotFound()
    if result.professional_id != user.id:
        return Unauthorized()
    else:
        professional_email = professional_service.get_professional_email_by_id(user.id)
        data = mailjet_service.create_email_for_deleting_ad(professional_email, user.name)
        mailjet.send.create(data)  

        return professional_ad_service.delete_professional_ad(ad_id)

@my_professional_ads_router.put('/{ad_id}/skillset')
def update_skill(ad_id: int, old_skillset: Skillset, new_skillset: Skillset, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized()

    result = professional_ad_service.get_professional_ad_by_ad_id(ad_id)
    if result is None:
        return NotFound()
    if result.professional_id != user.id:
        # return BadRequest()
        return Unauthorized()
    # new_ad.professional_id = user.id

    skillset = skill_service.update_skillset(old_skillset, new_skillset, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)

    professional_email = professional_service.get_professional_email_by_id(user.id)
    data = mailjet_service.create_email_for_update_of_ad(professional_email, user.name)
    mailjet.send.create(data)

    return skillset

@my_professional_ads_router.delete('/{ad_id}/skillset')
def remove_skill(ad_id, skillset: Skillset, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not isinstance(user, Professional):
        return Unauthorized()
    result = professional_ad_service.get_professional_ad_by_ad_id(ad_id)
    if result is None:
        return NotFound()
    if result.professional_id != user.id:
        return Unauthorized()
    
    professional_email = professional_service.get_professional_email_by_id(user.id)
    data = mailjet_service.create_email_for_deleting_ad(professional_email, user.name)
    mailjet.send.create(data)  

    return skill_service.delete_from_skillsets(skillset, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)
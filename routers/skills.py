from common.auth import get_user_or_raise_401
from fastapi import APIRouter, Header
from services import skill_service
from data.models import DBTable, DBColumn


skills_router = APIRouter(prefix='/skills')

@skills_router.get('/')
def get_skills_and_details(x_token: str = Header()):
    get_user_or_raise_401(x_token)
    full_list = skill_service.get_all_skills_info()

    return full_list

@skills_router.get('/{ad_id}')
def get_skillset_by_ad_id(ad_id: int, x_token: str = Header()):
    get_user_or_raise_401(x_token)

    
    skillset = skill_service.get_skillset_by_ad_id(ad_id, DBTable.PROFESSIONAL_ADS_SKILLSETS, DBColumn.PROFESSIONAL_AD_ID)
    
    return skillset

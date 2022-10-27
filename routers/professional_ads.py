from fastapi import APIRouter, Header


professional_ads_router = APIRouter()

@professional_ads_router.get('/')
def get_all_professional_ads():
    # user = get_user_or_raise_401(x_token)

    pass

@professional_ads_router.post('/', status_code=201)
def create_professional_ad():
    # user = get_user_or_raise_401(x_token)
    # if user is not Professional: retun Unauthorized()
    pass

@professional_ads_router.get('/{id}')
def get_professional_ad_by_id(id: int):
    pass

@professional_ads_router.put('/{id}')
def update_professional_ad_by_id(id: int):
    pass

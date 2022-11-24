from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from data.models import SearchResponse
from services import search_service

search_router = APIRouter(prefix='/search')

@search_router.get('/', response_model=list[SearchResponse])
def search_for_matches(slrt: str = None, skst: str = None, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    response = search_service.search(user=user, salary_threshold=slrt, skillset_threshold=skst)
    return response

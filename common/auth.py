from fastapi import HTTPException
from data.models import Company, Professional, Admin
from services.user_service import is_authenticated, from_token


def get_user_or_raise_401(token: str) -> Company | Professional | Admin:
    if not is_authenticated(token):
        raise HTTPException(status_code=401)

    return from_token(token)
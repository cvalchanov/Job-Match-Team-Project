from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized, NoContent
from data.models import AdminApprovals, Admin
from services import approval_service

approvals_router = APIRouter(prefix='/approvals')

@approvals_router.get('/', response_model=list[AdminApprovals])
def get_approvals(type: str | None = None, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user and isinstance(user, Admin):
        return approval_service.all(type=type)
    elif user and not isinstance(user, Admin):
        return Unauthorized()
    else:
        return BadRequest()

@approvals_router.get('/{id}')
def get_approval_by_id(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user and isinstance(user, Admin):
        approval = approval_service.get_by_id(id=id)
        return approval if approval else NotFound()
    elif user and not isinstance(user, Admin):
        return Unauthorized()
    else:
        return BadRequest()

@approvals_router.post('/')
def create_approval(approval: AdminApprovals, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user:
        approval = approval_service.create(approval=approval)
        return approval if approval else BadRequest()
    else:
        return Unauthorized()

@approvals_router.patch('/{id}')
def approve(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    approval = approval_service.get_by_id(id=id)
    if (user and approval) and isinstance(user, Admin):
        return approval_service.approve(approval=approval)
    elif (user and approval) and not isinstance(user,Admin):
        return Unauthorized()
    else:
        return BadRequest()

@approvals_router.delete('/{id}')
def delete_approval(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    approval = approval_service.get_by_id(id=id)
    if (user and approval) and isinstance(user, Admin):
        approval_service.delete(approval=approval)
        return NoContent()
    elif (user and approval) and not isinstance(user, Admin):
        return Unauthorized()
    else:
        return BadRequest()
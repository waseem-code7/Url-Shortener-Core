from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from starlette import status
from starlette.requests import Request

from common.dependencies import Authorization
from dtos.RequestDTOs import CreateUserRequest, ChangePasswordRequest
from registries.registry import ServiceRegistry
from services.user import UserService

router = APIRouter(tags=["User Routes"])

def get_user_service() -> UserService:
    return ServiceRegistry.get_registry("USER_SERVICE")

@router.post("/v1/users", status_code=status.HTTP_201_CREATED)
def create_user(body: CreateUserRequest = Body(), user_service: UserService = Depends(get_user_service)):
    try:
        user_service.create_new_user(body.__dict__)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/v1/users/change-password", status_code=status.HTTP_200_OK, dependencies=[Depends(Authorization.requires_login)])
def change_password(request: Request, body: ChangePasswordRequest = Body(), user_service: UserService = Depends(get_user_service)):
    try:
        session = request.state.session
        user_service.change_password(email=session["user"].get("email"), old_password=body.old_password, new_password=body.new_password)
        return {"Status": "Success"}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

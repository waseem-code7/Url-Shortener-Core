from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from starlette import status

from dtos.RequestDTOs import CreateUserRequest
from registries.registry import ServiceRegistry
from services.user import UserService

router = APIRouter()

def get_user_service() -> UserService:
    return ServiceRegistry.get_registry("USER_SERVICE")

@router.post("/v1/user", status_code=status.HTTP_201_CREATED)
def create_user(body: CreateUserRequest = Body(), user_service: UserService = Depends(get_user_service)):
    try:
        user_service.create_new_user(body.__dict__)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

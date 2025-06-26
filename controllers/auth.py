from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from starlette import status
from starlette.requests import Request

from registries.registry import ServiceRegistry
from services.auth import AuthService
from sessions.session import Session

router = APIRouter()

def get_auth_service() -> AuthService:
    return ServiceRegistry.get_registry("AUTH_SERVICE")

@router.post("v1/login")
def login(request: Request, body: dict = Body(), auth_service: AuthService = Depends(get_auth_service)):
    try:
        session: Session = request.state.session
        response = auth_service.verify_credentials(body.get("email_id"), body.get("password"))
        session["user"] = response.get("user")
        return {"Status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from common.dependencies import Authorization
from registries.registry import ServiceRegistry
from services.auth import AuthService
from sessions.session import Session

router = APIRouter(tags=["Authentication Routes"])

def get_auth_service() -> AuthService:
    return ServiceRegistry.get_registry("AUTH_SERVICE")

@router.post("/v1/login", status_code=status.HTTP_200_OK)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),  auth_service: AuthService = Depends(get_auth_service)):
    try:
        session: Session = request.state.session

        # TODO: Change this after frontend is implemented
        if session["user"]:
            return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

        response = auth_service.verify_credentials(form_data.username, form_data.password)
        session["user"] = response.get("user")
        return {"Status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

@router.post("/v1/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(Authorization.requires_login)])
def logout(request: Request):
    try:
        session: Session = request.state.session
        session.destroy()
        return {"Status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
from typing import Annotated

from fastapi import APIRouter, Body
from starlette.requests import Request

from sessions.session import Session

router = APIRouter()

@router.post("/login")
async def login_user(request: Request, body: dict = Body()):
    session: Session = request.state.session
    user_name = body.get("username")
    session["user_name"] = user_name
    session["user"] = {
        "name": "Waseem",
        "type": "MIDDLEWARE_TEST"
    }
    return {"Status": "Success"}

@router.post("/test_cookie")
async def login_user(request: Request, body: dict = Body()):
    session: Session = request.state.session
    print(session)
    return {"Status": "Success"}


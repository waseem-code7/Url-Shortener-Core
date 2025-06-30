from fastapi import HTTPException
from starlette import status
from starlette.requests import Request


class Authorization:

    @staticmethod
    def requires_login(request: Request):
        session = request.state.session
        if not session["user"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not logged in.")

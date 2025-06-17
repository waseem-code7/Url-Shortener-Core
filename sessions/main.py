import inspect
from fastapi.exceptions import HTTPException
from typing import Generic, Optional
from uuid import uuid4

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from sessions.abstractions.base_session_manager import BaseSessionManager
from sessions.generics.session_generics import T
from sessions.models.session_context import Cookie, SessionContext


class APISessions(BaseHTTPMiddleware, Generic[T]):

    def __init__(self, app, session_manager: BaseSessionManager[T], cookie: Cookie):
        super().__init__(app)
        self.app = app
        self.cookie= cookie
        self.session_manager = session_manager

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        session_id: str = request.cookies.get("session_id")
        get_res = self.session_manager.get_session(session_id)

        if inspect.iscoroutine(get_res):
            session_data: Optional[SessionContext[T]] = await get_res
        else:
            session_data: Optional[SessionContext[T]] = get_res

        request.state.session_data =  session_data.get_session_context()
        request.state.session.destroy_session: bool = False

        if not self.session_manager.verify(request, session_id, session_data.session):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden Request, Failed Verification")

        response: Response = await call_next(request)

        if request.state.session.destroy_session:
            des_res = self.session_manager.destroy(session_id)
            if inspect.iscoroutine(des_res):
                await des_res
            request.cookies.pop(__key="session_id")
        elif session_id is None or len(session_id) == 0:
            new_session_id = str(uuid4())
            new_session_data = request.state.session_data or None
            if new_session_data is not None:
                response.set_cookie(**self.cookie.__dict__, value=new_session_id)
                add_res = self.session_manager.add(new_session_id, new_session_data)
                if inspect.iscoroutine(add_res):
                    await add_res
        else:
            if session_data is not None:
                write_back_res = self.session_manager.write_back(session_id, session_data)
                if inspect.iscoroutine(write_back_res):
                    await write_back_res
        return response













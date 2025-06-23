from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from sessions.core import SessionManager


class SessionMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, session_manager: SessionManager):
        super().__init__(app)
        self.session_manager = session_manager


    def set_cookie_in_response(self, session_id: str, response: Response):
        cookie_conf = self.session_manager.get_cookie_config(session_id)
        response.set_cookie(**cookie_conf)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        session_id = request.cookies.get("session_id", None)
        session = await self.session_manager.load_session(session_id)
        request.state.session = session

        response: Response = await call_next(request)

        if session.is_new or session.modified:
            if session.is_new and self.session_manager.should_store_cookie(session):
                self.set_cookie_in_response(session.session_id, response)
            await self.session_manager.update_session(session)

        await self.session_manager.remove_inactive_session(session)

        return response

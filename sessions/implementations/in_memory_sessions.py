from threading import Lock
from typing import Union, Dict

from starlette.requests import Request

from sessions.abstractions.base_session_manager import BaseSessionManager
from sessions.generics.session_generics import T
from sessions.models.session_context import SessionContext


class InMemorySessionManager(BaseSessionManager):
    def __init__(self, config: dict, save_uninitialized: bool = False, max_sessions = 1000):
        super().__init__(config, save_uninitialized)
        self.max_sessions = max_sessions
        self._lock = Lock()
        self._sessions = Dict[str, SessionContext[T]]

    def connect(self):
        pass

    def add(self, session_id: str, session_data: SessionContext[T]):
        pass

    def destroy(self, session_id: str):
        pass

    def write_back(self, session_id: str, session_data: SessionContext[T]):
        pass

    def get_session(self, session_id: str) -> Union[None, SessionContext[T]]:
        pass

    def verify(self, request: Request, session_id: str, session_data: SessionContext[T]) -> bool:
        pass
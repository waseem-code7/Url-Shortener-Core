import json
from threading import Lock
from typing import Union, Dict

from starlette.requests import Request

from sessions.abstractions.base_session_manager import BaseSessionManager
from sessions.generics.session_generics import T
from sessions.models.session_context import SessionContext


class InMemorySessionManager(BaseSessionManager[T]):
    def __init__(self, config: dict):
        super().__init__(config)
        self._lock = Lock()
        self._sessions = Dict[str, str]
        self.connected = False

    def connect(self):
        self.connected = True

    def add(self, session_id: str, session_data: SessionContext[T]):
        with self._lock:
            self._sessions[session_id] = json.dumps(session_data.session.__dict__)

    def destroy(self, session_id: str):
        with self._lock:
            del self._sessions[session_id]


    def write_back(self, session_id: str, session_data: SessionContext[T]):
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id] = json.dumps(session_data.session)

    def get_session(self, session_id: str) -> Union[None, SessionContext[T]]:
        if session_id in self._sessions:
            session = self._sessions[session_id]
            return SessionContext[T](session=session)
        return None

    def verify(self, request: Request, session_id: str, session_data: SessionContext[T]) -> bool:
        pass
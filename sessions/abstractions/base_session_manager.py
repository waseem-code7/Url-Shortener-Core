from abc import ABC, abstractmethod
from typing import Generic, Union

from sessions.generics.session_generics import T
from sessions.models.session_context import SessionContext
from starlette.requests import Request


class BaseSessionManager(ABC, Generic[T]):

    def __init__(self, config: dict, save_uninitialized: bool = False):
        self.is_connected: False
        self.config = config
        self.save_uninitialized = save_uninitialized

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add(self, session_id: str, session_data: SessionContext[T]):
        pass

    @abstractmethod
    def destroy(self, session_id: str):
        pass

    @abstractmethod
    def write_back(self, session_id: str, session_data: SessionContext[T]):
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Union[None, SessionContext[T]]:
        pass

    @abstractmethod
    def verify(self, request: Request, session_id: str, session_data: SessionContext[T]) -> bool:
        return True



from datetime import datetime
from typing import Generic, Union, Optional
from enum import Enum

from sessions.generics.session_generics import T


class SameSite(Enum):
    NONE = "NONE"
    LAX = "LAX"
    STRICT = "STRICT"

class Cookie:
    key: str
    value: str = ""
    max_age: Optional[int] = None
    expires: Union[datetime, str, int, None] = None
    path: Optional[str] = "/"
    domain: Optional[str] = None
    secure: bool = True
    httponly: bool = True
    samesite: SameSite = SameSite.LAX

class SessionContext(Generic[T]):
    def __init__(self, session: T):
        self.session = session

    def get_session_context(self) -> T:
        return self.session

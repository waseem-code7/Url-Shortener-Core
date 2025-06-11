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
    session_data: T

from dataclasses import dataclass
from typing import Optional

from sessions.id_generators.base import SessionIDGenerator
from sessions.serializers.base import SessionSerializer
from sessions.stores.base import SessionStore


@dataclass
class SessionConfig:
    """Configuration for session management"""
    store: SessionStore = None
    serializer: SessionSerializer = None
    id_generator: SessionIDGenerator = None
    cookie_name: str = "session_id"
    cookie_max_age: Optional[int] = 86400  # 24 hours
    cookie_path: str = "/"
    cookie_domain: Optional[str] = None
    cookie_secure: bool = False
    cookie_httponly: bool = True
    cookie_samesite: str = "lax"
    auto_save: bool = True
    rolling: bool = False  # Reset expiry on each request

    def __post_init__(self):
        if self.store is None:
            self.store = MemoryStore()
        if self.serializer is None:
            self.serializer = JSONSerializer()
        if self.id_generator is None:
            self.id_generator = SecureRandomGenerator()

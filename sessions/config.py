from dataclasses import dataclass
from typing import Optional, Literal, Union

from sessions.id_generators.base import SessionIDGenerator
from sessions.id_generators.uuidGenerator import SecureRandomGenerator
from sessions.serializers.JSONSerializer import JSONSerializer
from sessions.serializers.base import SessionSerializer
from sessions.stores.MemoryStore import MemoryStore
from sessions.stores.base import SessionStore


@dataclass
class SessionConfig:
    """Configuration for session management"""
    store: SessionStore = None
    serializer: SessionSerializer = None
    id_generator: SessionIDGenerator = None
    ttl_in_sec: int = 86400
    cookie_name: str = "session_id"
    cookie_max_age: Optional[int] = 86400  # 24 hours
    cookie_path: str = "/"
    cookie_domain: Optional[str] = None
    cookie_secure: bool = True
    cookie_httponly: bool = True
    cookie_samesite: Union[Literal["lax", "strict", "none"], None] = "lax"
    rolling: bool = False  # Reset expiry on each request
    increase_interval_on_touch: int = 10000 # applicable only is rolling is set to True
    save_uninitialized = False

    def __post_init__(self):
        if self.store is None:
            self.store = MemoryStore()
        if self.serializer is None:
            self.serializer = JSONSerializer()
        if self.id_generator is None:
            self.id_generator = SecureRandomGenerator()

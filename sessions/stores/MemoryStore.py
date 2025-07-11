import asyncio
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Callable, Union
from sessions.stores.base import SessionStore
from concurrent.futures import ThreadPoolExecutor

class MemoryStore(SessionStore):
    """In-memory session store with TTL support"""
    _instance = None
    _lock = threading.Lock()

    def __init__(self, should_delete_expired_sessions = True, async_cleanup_task: Union[None, Callable] = None, expiration_loop_interval = 60, debug=False):
        if self._initialized:
            return

        self._sessions: Dict[str, str] = {}
        self._expiry: Dict[str, datetime] = {}

        self.expiration_loop_interval = expiration_loop_interval # check of expired session every 60 sec
        self.debug = True
        self.should_delete_expired_sessions = should_delete_expired_sessions
        self.async_cleanup_task = async_cleanup_task
        self.start_cleanup()
        self._initialized = True


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._initialized = False
        return cls._instance


    def _get_expired_sessions(self):
        now = datetime.now()
        expired_sessions = [session_id for session_id, ttl in self._expiry.items() if ttl <= now]
        if self.debug:
            print(f"Found {len(expired_sessions)}")
        return expired_sessions


    def start_cleanup(self):
        if self.debug:
            print("Starting session expiration loop")

        if self.async_cleanup_task is None and self.should_delete_expired_sessions:
            self.async_cleanup_task = asyncio.create_task(self._cleanup_expired_sessions())


    async def _cleanup_expired_sessions(self):
        while True:
            try:
                if self.debug:
                    print("Attempting to get expired sessions")

                with ThreadPoolExecutor(max_workers=1) as executor:
                    futures = [executor.submit(self._get_expired_sessions)]

                expired_session_ids = futures[0].result()

                for session_id in expired_session_ids:
                    del self._sessions[session_id]
                    del self._expiry[session_id]

                await asyncio.sleep(self.expiration_loop_interval)
            except asyncio.CancelledError:
                if self.debug:
                    print("Cancel error occurred in expired session cleanup")
                self.cleanup_task = None
                break

    async def get(self, session_id: str):
        if await self.exists(session_id):
            return self._sessions[session_id]
        return None

    async def put(self, session_id: str, session_data: str, is_new: bool, ttl: Optional[int]) -> None:
        if session_id is None or len(session_id) == 0:
            return
        self._sessions[session_id] = session_data
        if ttl and is_new:
            self._expiry[session_id] = datetime.now() + timedelta(seconds=ttl)

    async def touch(self, session_id: str, ttl: int) -> None:
        if self.exists(session_id):
            self._expiry[session_id] = datetime.now() + timedelta(seconds=ttl)

    async def delete(self, session_id: str) -> None:
        if await self.exists(session_id):
            del self._sessions[session_id]
            del self._expiry[session_id]

    async def exists(self, session_id: str) -> bool:
        if session_id in self._sessions:
            return True
        return False




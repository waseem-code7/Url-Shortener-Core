import asyncio
from datetime import datetime, timedelta
from os.path import exists
from threading import Thread
from typing import Optional, Any, Dict

from sessions.serializers.JSONSerializer import JSONSerializer
from sessions.serializers.base import SessionSerializer
from sessions.stores.base import SessionStore
from concurrent.futures import ThreadPoolExecutor

class MemoryStore(SessionStore):
    """In-memory session store with TTL support"""

    def __init__(self, serializer: Optional[SessionSerializer] = None):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._expiry: Dict[str, datetime] = {}
        self.serializer = serializer or JSONSerializer()
        self.expiration_loop_interval = 60 # check of expired session every 60 sec
        self.debug = False
        self.cleanup_task = None
        self.start_cleanup()


    def _get_expired_sessions(self):
        now = datetime.now()
        expired_sessions = [session_id for session_id, ttl in self._expiry.items() if ttl <= now]
        if self.debug:
            print(f"Found {len(expired_sessions)}")
        return expired_sessions


    def start_cleanup(self):
        if self.debug:
            print("Starting session expiration loop")

        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup_expired_sessions())


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
        if self.exists(session_id):
            return self._sessions[session_id]
        return None

    async def put(self, session_id: str, session_data: Dict[str, Any], ttl: Optional[int]) -> None:
        if not exists(session_id):
            self._sessions[session_id] = session_data
            if ttl:
                self._expiry[session_id] = datetime.now() + timedelta(seconds=ttl)

    async def touch(self, session_id: str, ttl: int) -> None:
        if self.exists(session_id):
            self._expiry[session_id] = datetime.now() + timedelta(seconds=ttl)

    async def delete(self, session_id: str) -> None:
        if self.exists(session_id):
            del self._sessions[session_id]
            del self._expiry[session_id]

    async def exists(self, session_id: str) -> bool:
        if session_id in self._sessions:
            return True
        return False




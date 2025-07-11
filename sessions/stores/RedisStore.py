import threading
from typing import Union, Dict, Any, Optional
import redis.asyncio as redis
from redis.asyncio.cluster import ClusterNode
from sessions.stores.base import SessionStore


class RedisStore(SessionStore):
    _instance = None
    _lock = threading.Lock()

    def __init__(self, host: str, port: int, db: int, cluster_nodes: Optional[list[ClusterNode]], cluster_mode=False, user_session_store: str = "sessions"):
        if self._initialized:
            return
        self.client = None

        if not cluster_mode:
            self.client = redis.Redis(host=host, port=port, db=db)
        else:
            self.client = redis.RedisCluster(startup_nodes=cluster_nodes, decode_responses=False)
        self.user_session_store = user_session_store

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._initialized = False
        return cls._instance

    def get_store_key(self, session_id):
        return self.user_session_store + ":" + session_id

    async def get(self, session_id: str):
        key = self.get_store_key(session_id)
        return await self.client.get(key)

    async def put(self, session_id: str, session_data: Union[Dict[str, Any], str], is_new: bool,
                  ttl: Optional[int]) -> None:
        if session_id is None or len(session_id) == 0:
            return
        key = self.get_store_key(session_id)
        await self.client.set(key, session_data)
        if is_new:
            await self.client.expire(key, ttl)

    async def touch(self, session_id: str, ttl: int) -> None:
        if await self.exists(session_id):
            key = self.get_store_key(session_id)
            await self.client.expire(key, ttl)

    async def delete(self, session_id: str) -> None:
        key = self.get_store_key(session_id)
        await self.client.delete(key)

    async def exists(self, session_id: str) -> bool:
        key = self.get_store_key(session_id)
        return await self.client.exists(key)
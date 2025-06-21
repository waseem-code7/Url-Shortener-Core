from abc import ABC, abstractmethod
from typing import Dict, Optional


class Session(ABC):
    """Abstract base class for session storage"""

    @abstractmethod
    async def get(self, session_id: str):
        """Retrieve session data by ID"""
        pass

    @abstractmethod
    async def put(self, session_id: str, session_data: Dict[str, any], ttl: Optional[int]) -> None:
        """Store session data with optional TTL in seconds"""
        pass

    @abstractmethod
    async def touch(self, session_id: str) -> None:
        """Update session expiration time"""
        pass

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        """Delete session by ID"""
        pass

    @abstractmethod
    async def exists(self, session_id: str) -> bool:
        """Check if session exists"""
        pass
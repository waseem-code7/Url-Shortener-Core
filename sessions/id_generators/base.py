from abc import ABC, abstractmethod

class SessionIDGenerator(ABC):
    """Abstract base class for session ID generation"""

    @abstractmethod
    async def generate(self):
        """Generate a new session ID"""
        pass
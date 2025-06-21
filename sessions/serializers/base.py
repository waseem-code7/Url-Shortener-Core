from abc import ABC, abstractmethod
from typing import Dict, Union, Any


class SessionSerializer(ABC):
    """Abstract base class for session data serialization"""

    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> Union[str, bytes]:
        """Serialize session data"""
        pass

    @abstractmethod
    def deserialize(self, data: Union[str, bytes]) -> Dict[str, Any]:
        """Deserialize session data"""
        pass
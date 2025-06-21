from abc import ABC, abstractmethod
from typing import Dict, Union


class SessionSerializer(ABC):

    @abstractmethod
    def serialize(self, data: Dict[str, any]) -> Union[str, bytes]:
        pass

    @abstractmethod
    def deserialize(self) -> Dict[str, any]:
        pass
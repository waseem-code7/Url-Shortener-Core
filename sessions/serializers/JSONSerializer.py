import json
from typing import Dict, Union, Any

from sessions.serializers.base import SessionSerializer


class JSONSerializer(SessionSerializer):
    """JSON-based session serializer"""

    def serialize(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, default=str)

    def deserialize(self, data: Union[str, bytes]) -> Dict[str, Any]:
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return json.loads(data)
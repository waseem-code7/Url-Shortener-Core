import uuid

from sessions.id_generators.base import SessionIDGenerator


class UUIDGenerator(SessionIDGenerator):
    """UUID-based session ID generator"""

    def generate(self) -> str:
        return str(uuid.uuid4())
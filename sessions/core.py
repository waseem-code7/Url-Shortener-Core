from typing_extensions import Optional

from sessions.config import SessionConfig
from sessions.session import Session


class SessionManager:

    def __init__(self, config: SessionConfig):
        self.config = config


    async def load_session(self, session_id: Optional[str]):
        """Load session from store or create new one"""

        does_session_exist = False

        if session_id:
            does_session_exist = await self.config.store.exists(session_id)

        if does_session_exist:
            session_data_db = await self.config.store.get(session_id)
            deserialized_data: dict = self.config.serializer.deserialize(session_data_db)
            session = Session(session_id=session_id, data=deserialized_data, is_new=False)
        else:
            session_id = await self.config.id_generator.generate()
            session = Session(session_id=session_id, data={}, is_new=True)

        return session

    async def delete_session(self, session_id: str):
        """Delete session from store if exists"""

        if session_id:
            await self.config.store.delete(session_id)

    async def touch_session(self, session_id: str):
        """Increase session expiry time"""

        if session_id and self.config.rolling:
            await self.config.store.touch(session_id, self.config.ttl_in_sec)

    async def update_session(self, session: Session):
        """Update session data"""

        session_id = session.session_id
        if session_id:
            updated_session_data = session.data
            serialized_data = self.config.serializer.serialize(updated_session_data)
            await self.config.store.put(session_id, serialized_data, self.config.ttl_in_sec)


    async def remove_inactive_session(self, session: Session):
        """Remove the inactive session"""

        session_id = session.session_id
        is_active_session = session.is_active

        if session_id and not is_active_session:
            await self.config.store.delete(session_id)



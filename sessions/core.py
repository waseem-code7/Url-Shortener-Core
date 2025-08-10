from typing_extensions import Optional, Literal

from sessions.config import SessionConfig
from sessions.session import Session


class SessionManager:

    def __init__(self, config: SessionConfig):
        self.config = config


    async def load_session(self, session_id: Optional[str]) -> Session:
        """Load session from store or create new one"""

        does_session_exist = False

        if session_id:
            does_session_exist = await self.config.store.exists(session_id)

        if does_session_exist:
            session_data_db = await self.config.store.get(session_id)
            deserialized_data: dict = self.config.serializer.deserialize(session_data_db)
            session = Session(session_id=session_id, data=deserialized_data, is_new=False)

        else:
            session_id = self.config.id_generator.generate()
            await self.config.store.put(session_id=session_id, session_data=self.config.serializer.serialize({}), is_new=True, ttl=self.config.ttl_in_sec)
            session = Session(session_id=session_id, data={}, is_new=True)

        return session

    async def delete_session(self, session_id: str):
        """Delete session from store if exists"""

        if session_id:
            await self.config.store.delete(session_id)

    async def touch_session(self, session_id: str):
        """Reset session expiry time"""

        if session_id:
            await self.config.store.touch(session_id, self.config.reset_interval_on_touch)

    async def update_session(self, session: Session) -> None:
        """Update session data"""
        if len(session) == 0 and self.config.save_uninitialized == False:
            return

        session_id = session.session_id
        if session_id:
            updated_session_data = session.data
            serialized_data = self.config.serializer.serialize(updated_session_data)
            await self.config.store.put(session_id=session_id, session_data=serialized_data, is_new=False, ttl=None)
            if self.config.rolling:
                await self.touch_session(session_id)

    async def remove_inactive_session(self, session: Session):
        """Remove the inactive session"""

        session_id = session.session_id
        is_active_session = session.is_active

        if session_id and not is_active_session:
            await self.config.store.delete(session_id)
            return True

        return False

    def should_store_cookie(self, session: Session):
        """Check if cookie can be stored in response"""

        if self.config.save_uninitialized:
            return True
        return len(session) != 0

    def get_cookie_config(self, session_id, request_type: Literal["CREATE", "DELETE"]):
        """Return the cookie config"""

        if request_type == "CREATE":
            return {
                "key": "session_id",
                "value": session_id,
                "max_age": self.config.cookie_max_age,
                "path": self.config.cookie_path,
                "domain": self.config.cookie_domain,
                "secure": self.config.cookie_secure,
                "httponly": self.config.cookie_httponly,
                "samesite": self.config.cookie_samesite
            }
        else:
            return {
                "key": "session_id",
                "path": self.config.cookie_path,
                "domain": self.config.cookie_domain,
                "secure": self.config.cookie_secure,
                "httponly": self.config.cookie_httponly,
                "samesite": self.config.cookie_samesite
            }

import json

import redis

from rickroll.config import settings
from rickroll.models import GameSession


class RedisDB:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True,
        )

    def set_link(self, short_code: str, original_url: str) -> bool:
        try:
            return bool(self.redis_client.set(f"link:{short_code}", original_url))
        except Exception:
            return False

    def get_link(self, short_code: str) -> str | None:
        try:
            return self.redis_client.get(f"link:{short_code}")
        except Exception:
            return None

    def set_game_session(self, session: GameSession) -> bool:
        try:
            session_data = session.model_dump_json()
            return bool(
                self.redis_client.set(
                    f"game:{session.session_id}", session_data, ex=3600
                )
            )
        except Exception:
            return False

    def get_game_session(self, session_id: str) -> GameSession | None:
        try:
            session_data = self.redis_client.get(f"game:{session_id}")
            if session_data:
                return GameSession.model_validate_json(session_data)
            return None
        except Exception:
            return None

    def delete_game_session(self, session_id: str) -> bool:
        try:
            return bool(self.redis_client.delete(f"game:{session_id}"))
        except Exception:
            return False

    def health_check(self) -> bool:
        try:
            return self.redis_client.ping()
        except Exception:
            return False


db = RedisDB()

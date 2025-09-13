from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class LinkRequest(BaseModel):
    url: HttpUrl


class LinkResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str


class GameStartResponse(BaseModel):
    session_id: str
    total_links: int


class GameLinkResponse(BaseModel):
    link_index: int
    short_code: str
    total_links: int
    coins: int


class GuessType(str, Enum):
    NOT_RICKROLL = "not_rickroll"
    CONTINUE = "continue"


class GameGuessRequest(BaseModel):
    session_id: str
    link_index: int
    guess: GuessType


class GameGuessResponse(BaseModel):
    correct: bool
    is_rickroll: bool
    original_url: str | None = None
    coins: int
    game_over: bool = False
    won: bool = False
    flag: str | None = None
    is_rickrolled: bool = False


class GameSession(BaseModel):
    session_id: str
    start_time: datetime
    current_index: int
    coins: int
    links: list[dict]
    is_active: bool = True

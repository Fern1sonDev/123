import random

from fastapi import APIRouter, HTTPException, Request

from rickroll.config import settings
from rickroll.database import db
from rickroll.models import (
    GameGuessRequest,
    GameGuessResponse,
    GameLinkResponse,
    GameSession,
    GameStartResponse,
    GuessType,
)
from rickroll.utils import (
    create_game_links,
    generate_session_id,
    get_time,
)

router = APIRouter(prefix="/api/game", tags=["game"])


@router.post("/start", response_model=GameStartResponse)
async def start_game():
    session_id = generate_session_id()
    start_time_ms, start_time_dt = get_time()

    random.seed(start_time_ms)

    game_links = create_game_links()

    session = GameSession(
        session_id=session_id,
        start_time=start_time_dt,
        current_index=0,
        coins=0,
        links=game_links,
        is_active=True,
    )

    success = db.set_game_session(session)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось создать сессию")

    return GameStartResponse(
        session_id=session_id,
        total_links=settings.total_links,
    )


@router.get("/link/{session_id}", response_model=GameLinkResponse)
async def get_game_link(session_id: str):
    session = db.get_game_session(session_id)

    if not session or not session.is_active:
        raise HTTPException(status_code=404, detail="Сессия не найдена или не активна")

    if session.current_index >= len(session.links):
        raise HTTPException(status_code=400, detail="Игра закончена")

    current_link = session.links[session.current_index]

    return GameLinkResponse(
        link_index=session.current_index,
        short_code=current_link["short_code"],
        total_links=settings.total_links,
        coins=session.coins,
    )


@router.post("/guess", response_model=GameGuessResponse)
async def make_guess(data: GameGuessRequest, request: Request):
    session = db.get_game_session(data.session_id)

    if not session or not session.is_active:
        raise HTTPException(status_code=404, detail="Сессия не найдена или не активна")

    if data.link_index != session.current_index:
        raise HTTPException(status_code=400, detail="Неверный индекс ссылки")

    if session.current_index >= len(session.links):
        raise HTTPException(status_code=400, detail="Игра закончена")

    current_link = session.links[session.current_index]
    is_rickroll = current_link["is_rickroll"]

    correct = False
    game_over = False

    is_rickrolled = False

    if data.guess == GuessType.NOT_RICKROLL:
        if is_rickroll:
            game_over = True
            session.is_active = False
            is_rickrolled = True
        else:
            correct = True
            session.coins += 1

    elif data.guess == GuessType.CONTINUE:
        correct = False

    session.current_index += 1

    if session.current_index >= settings.total_links:
        game_over = True
        session.is_active = False

    won = game_over and session.coins >= settings.winning_coins
    flag = ("alfa{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}" if won else None)

    if game_over and not won:
        db.delete_game_session(data.session_id)
    else:
        db.set_game_session(session)

    original_url_to_return = (
        current_link["original_url"] if data.guess == GuessType.NOT_RICKROLL else None
    )

    return GameGuessResponse(
        correct=correct,
        is_rickroll=is_rickroll,
        original_url=original_url_to_return,
        coins=session.coins,
        game_over=game_over,
        won=won,
        flag=flag,
        is_rickrolled=is_rickrolled,
    )

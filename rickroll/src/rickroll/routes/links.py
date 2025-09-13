from fastapi import APIRouter, HTTPException

from rickroll.config import settings
from rickroll.database import db
from rickroll.models import LinkRequest, LinkResponse
from rickroll.utils import generate_short_code, validate_url

router = APIRouter(prefix="/api/links", tags=["links"])


@router.post("/shorten", response_model=LinkResponse)
async def shorten_link(request: LinkRequest):
    url_str = str(request.url)

    if not validate_url(url_str):
        raise HTTPException(status_code=400, detail="Неверный URL")

    short_code = generate_short_code()

    success = db.set_link(short_code, url_str)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось сохранить ссылку")

    return LinkResponse(
        short_code=short_code, original_url=url_str, short_url=f"/s/{short_code}"
    )


@router.get("/{short_code}")
async def get_link(short_code: str):
    original_url = db.get_link(short_code)

    if not original_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    return {"url": original_url}

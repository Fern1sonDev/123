import os
import random
import string
import time
import uuid
from datetime import datetime

from rickroll.config import settings


def generate_short_code() -> str:
    letters = string.ascii_lowercase
    code = "".join(random.choice(letters) for _ in range(9))

    return code


def generate_session_id() -> str:
    return str(uuid.uuid4())


def get_time() -> tuple[int, datetime]:
    cur_time_ms = int(time.time() * 1000)
    return cur_time_ms, datetime.now().replace(microsecond=0)


def read_links_from_file(file_path: str = "data/links.txt") -> list[str]:
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r") as f:
            links = [line.strip() for line in f if line.strip()]
        return links
    except Exception:
        return []


def create_game_links() -> list[dict[str, any]]:
    links = []

    file_links = read_links_from_file(settings.game_links_file)

    if len(file_links) >= 25:
        random_file_links = random.sample(file_links, 25)
    else:
        random_file_links = file_links + ["https://example.com"] * (
            25 - len(file_links)
        )

    for _ in range(25):
        short_code = generate_short_code()
        links.append(
            {
                "short_code": short_code,
                "is_rickroll": True,
                "original_url": settings.rickroll_url,
            }
        )

    for url in random_file_links:
        short_code = generate_short_code()
        links.append(
            {"short_code": short_code, "is_rickroll": False, "original_url": url}
        )

    random.shuffle(links)

    return links


def validate_url(url: str) -> bool:
    return url.startswith(("http://", "https://")) and len(url) > 10

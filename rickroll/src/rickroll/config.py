from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False

    winning_coins: int = 20
    total_links: int = 50
    rickroll_links: int = 25
    stored_links: int = 25

    rickroll_url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    game_links_file: str = "data/links.txt"

    class Config:
        env_file = ".env"


settings = Settings()

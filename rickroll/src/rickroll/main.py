import uvicorn

from rickroll.app import app
from rickroll.config import settings


def main():
    print("🚀 Starting FastAPI server")

    uvicorn.run(
        "rickroll.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()

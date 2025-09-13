from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from rickroll.config import settings
from rickroll.database import db
from rickroll.routes import game, links

app = FastAPI(
    title="RickRoll Link Shortener",
    description="",
    version="1.0.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(links.router)
app.include_router(game.router)


@app.get("/")
async def root():
    return {"message": "RickRoll Link Shortener API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    redis_healthy = db.health_check()

    if not redis_healthy:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    return {"status": "healthy", "redis": "connected"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if settings.debug:
        import traceback

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error": str(exc),
                "traceback": traceback.format_exc(),
            },
        )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

from fastapi import FastAPI
from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(title="JobInsight AI API", version="0.1.0")
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "backend"}


@app.get("/api/v1/health")
def api_health_check() -> dict[str, str]:
    return {"status": "ok", "database": settings.database_url.split("@")[-1] if settings.database_url else "not-configured"}

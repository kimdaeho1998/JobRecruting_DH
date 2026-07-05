from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="JobInsight AI API", version="0.1.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "backend"}


@app.get("/api/v1/health")
def api_health_check() -> dict[str, str]:
    return {"status": "ok", "database": settings.database_url.split("@")[-1] if settings.database_url else "not-configured"}

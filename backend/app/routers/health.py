from fastapi import APIRouter

from app.db.mongodb import get_database

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_route() -> dict:
    db = get_database()
    await db.command("ping")
    return {"status": "ok", "database": "connected", "service": "VerifyIT API"}

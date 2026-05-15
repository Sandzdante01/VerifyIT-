from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.indexes import create_indexes
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.routers import auth, claims, feedback, health, settings, sources
from app.services.source_service import seed_default_sources


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    await create_indexes()
    await seed_default_sources()
    yield
    await close_mongo_connection()


def create_app() -> FastAPI:
    config = get_settings()
    app = FastAPI(title="VerifyIT API", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(claims.router, prefix="/api")
    app.include_router(sources.router, prefix="/api")
    app.include_router(feedback.router, prefix="/api")
    app.include_router(settings.router, prefix="/api")
    return app


app = create_app()

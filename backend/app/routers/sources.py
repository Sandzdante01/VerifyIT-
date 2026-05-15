from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.schemas.auth_schema import MessageResponse
from app.schemas.source_schema import SourceListResponse, SourceResponse
from app.services.source_service import get_source, list_sources, seed_default_sources

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=SourceListResponse)
async def sources_route(topic: str | None = None, _: dict = Depends(get_current_user)) -> SourceListResponse:
    return SourceListResponse(items=await list_sources(topic))


@router.post("/seed/defaults", response_model=MessageResponse)
async def seed_route(_: dict = Depends(get_current_user)) -> MessageResponse:
    await seed_default_sources()
    return MessageResponse(message="Default sources seeded")


@router.get("/{source_id}", response_model=SourceResponse)
async def source_detail_route(source_id: str, _: dict = Depends(get_current_user)) -> SourceResponse:
    source = await get_source(source_id)
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return source

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.feed_service import FeedService
from app.schemas.post_query import PostQuery

router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

@router.get("/")
async def get_feed(
    query: PostQuery = Depends(),
    db: AsyncSession = Depends(get_db)
):

    return await FeedService.get_feed_with_metadata(
        db,
        query
    )


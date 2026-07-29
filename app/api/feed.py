from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.feed_service import FeedService
from app.schemas.post_query import PostQuery
from app.schemas.pegination import PaginationResponse
from app.schemas.post import PostResponse

router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

@router.get(
    "/",
    response_model=PaginationResponse[PostResponse]
)
async def get_feed(
    query: PostQuery = Depends(),
    db: AsyncSession = Depends(get_db)
):

    return await FeedService.get_feed_with_metadata(
        db,
        query
    )


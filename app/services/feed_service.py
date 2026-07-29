from sqlalchemy.ext.asyncio import AsyncSession
from math import ceil
from app.repositories.post_repository import PostRepository
from app.schemas.post_query import PostQuery

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.post_repository import PostRepository
from app.schemas.post_query import PostQuery

from app.schemas.pegination import PaginationResponse
from app.schemas.post import PostResponse


class FeedService:

    @staticmethod
    async def get_feed(
        db: AsyncSession,
        query: PostQuery
    ):
        return await PostRepository.get_feed(
            db,
            query
        )


   

    @staticmethod
    async def get_feed_with_metadata(
        db: AsyncSession,
        query: PostQuery
    ):

        posts = await PostRepository.get_feed(
            db,
            query
        )

        total_items = await PostRepository.count_posts(
            db,
            query
        )

        total_pages = ceil(
            total_items / query.limit
        )

        return PaginationResponse[PostResponse](

            page = query.page,

            limit = query.limit,

            total_items = total_items,

            total_pages = total_pages,

            has_next = query.page < total_pages,

            has_previous = query.page > 1,

            items = posts

        )
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.post_repository import PostRepository
from app.schemas.post_query import PostQuery

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.post_repository import PostRepository
from app.schemas.post_query import PostQuery


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

        return {
            "page": query.page,
            "limit": query.limit,
            "items": posts
        }
from sqlalchemy import select , or_ ,func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.post import Post, PostStatus
from app.schemas.post_query import PostQuery
from app.models.user import User
from app.models.like import Like

class PostRepository:

    @staticmethod
    async def create(db: AsyncSession, post: Post):
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_by_id(db: AsyncSession, post_id: int):
        result = await db.execute(
            select(Post).where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str):
        result = await db.execute(
            select(Post).where(Post.slug == slug)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, post: Post):
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def delete(db: AsyncSession, post: Post):
        await db.delete(post)
        await db.commit()

    @staticmethod
    async def list_published(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
    ):
        result = await db.execute(
            select(Post)
            .where(Post.status == PostStatus.PUBLISHED)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def list_by_author(
        db: AsyncSession,
        author_id: int,
        skip: int = 0,
        limit: int = 10
    ):
        result = await db.execute(
            select(Post)
            .where(Post.author_id == author_id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def search_posts(
        db: AsyncSession,
        search: str,
        skip: int = 0,
        limit: int = 10,
    ):
        result = await db.execute(
            select(Post)
            .where(
                Post.status == PostStatus.PUBLISHED,
                or_(
                Post.title.ilike(f"%{search}%"),
                Post.content.ilike(f"%{search}%")
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Post.created_at.desc())
        )

        return result

    @staticmethod
    async def get_feed(
        db: AsyncSession,
        query: PostQuery
    ):
        statement = (
            select(Post)
            .options(
                selectinload(Post.author)
            )
        )

        if query.published is not None:
            statement = statement.where(
                Post.is_published == query.published
            )

        if query.search:
            statement = statement.where(
                Post.title.ilike(
                    f"%{query.search}%"
                )
            )

        if query.author:
            statement = (
                statement
                .join(User)
                .where(
                    User.username == query.author
                )
            )

        if query.sort == "newest":
            statement = statement.order_by(
                desc(Post.created_at)
            )

        elif query.sort == "oldest":
            statement = statement.order_by(
                asc(Post.created_at)
            )

        offset = (
            query.page - 1
        ) * query.limit

        statement = (
            statement
            .offset(offset)
            .limit(query.limit)
        )

        result = await db.execute(
            statement
        )

        return result.scalars().all()

    
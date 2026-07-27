from sqlalchemy import select , or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post, PostStatus


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
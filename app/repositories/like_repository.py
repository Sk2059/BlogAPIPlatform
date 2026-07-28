from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.like import Like

class LikeRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        like: Like
    ):
        db.add(like)
        await db.commit()
        await db.refresh(like)
        return like

    @staticmethod
    async def get_by_user_and_post(
        db: AsyncSession,
        user_id: int,
        post_id: int
    ):
        result = await db.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.post_id == post_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        like: Like
    ):
        await db.delete(like)
        await db.commit()

    @staticmethod
    async def count_post_likes(
        db: AsyncSession,
        post_id: int
    ):
        result = await db.execute(
            select(func.count())
            .select_from(Like)
            .where(Like.post_id == post_id)
        )
        return result.scalar()

    @staticmethod
    async def is_liked(
        db: AsyncSession,
        user_id: int,
        post_id: int
    ):
        like = await LikeRepository.get_by_user_and_post(
            db,
            user_id,
            post_id
        )

        return like is not None

    @staticmethod
    async def get_post_likes(
        db: AsyncSession,
        post_id: int
    ):
        result = await db.execute(
            select(Like).where(
                Like.post_id == post_id
            )
        )
        return result.scalars().all()
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment

class CommentRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        comment: Comment
    ):
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment


    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        comment_id: int
    ):
        result = await db.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_post_comments(
        db: AsyncSession,
        post_id: int
    ):
        result = await db.execute(
            select(Comment)
            .where(
                Comment.post_id == post_id,
                Comment.parent_id.is_(None)
            )
            .options(
                selectinload(Comment.author),
                selectinload(Comment.replies)
            )
            .order_by(Comment.created_at.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_replies(
        db: AsyncSession,
        parent_id: int
    ):
        result = await db.execute(
            select(Comment)
            .where(Comment.parent_id == parent_id)
            .options(
                selectinload(Comment.author)
            )
            .order_by(Comment.created_at.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        comment: Comment
    ):

        await db.commit()

        await db.refresh(comment)

        return comment

    @staticmethod
    async def delete(
        db: AsyncSession,
        comment: Comment
    ):

        await db.delete(comment)

        await db.commit()

    @staticmethod
    async def count_post_comments(
        db: AsyncSession,
        post_id: int
    ):
        result = await db.execute(
            select(func.count())
            .select_from(Comment)
            .where(Comment.post_id == post_id)
        )
        return result.scalar()

    @staticmethod
    async def count_replies(
        db: AsyncSession,
        parent_id: int
    ):
        result = await db.execute(
            select(func.count())
            .select_from(Comment)
            .where(Comment.parent_id == parent_id)
        )
        return result.scalar()
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.like import Like
from app.models.user import User

from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository

from app.schemas.like import (
    ToggleLikeResponse,
    LikeStatusResponse,
)

class LikeService:
    @staticmethod
    async def verify_post_exists(
        db: AsyncSession,
        post_id: int
    ):

        post = await PostRepository.get_by_id(
            db,
            post_id
        )

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        return post

    @staticmethod
    async def like_post(
        db: AsyncSession,
        post_id: int,
        current_user: User
    ):
        await LikeService.verify_post_exists(
            db,
            post_id
        )
        existing = await LikeRepository.get_by_user_and_post(
            db,
            current_user.id,
            post_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="You already liked this post."
            )
        like = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        return await LikeRepository.create(
            db,
            like
        )

    @staticmethod
    async def unlike_post(
        db: AsyncSession,
        post_id: int,
        current_user: User
    ):
        like = await LikeRepository.get_by_user_and_post(
            db,
            current_user.id,
            post_id
        )
        if like is None:
            raise HTTPException(
                status_code=404,
                detail="Like not found"
            )
        await LikeRepository.delete(
            db,
            like
        )
        return {
            "message": "Post unliked successfully"
        }

    @staticmethod
    async def toggle_like(
        db: AsyncSession,
        post_id: int,
        current_user: User
    ):

        await LikeService.verify_post_exists(
            db,
            post_id
        )

        existing = await LikeRepository.get_by_user_and_post(
            db,
            current_user.id,
            post_id
        )

        if existing:

            await LikeRepository.delete(
                db,
                existing
            )

            total = await LikeRepository.count_post_likes(
                db,
                post_id
            )

            return ToggleLikeResponse(
                liked=False,
                total_likes=total,
                message="Post unliked successfully"
            )

        like = Like(
            user_id=current_user.id,
            post_id=post_id
        )

        await LikeRepository.create(
            db,
            like
        )

        total = await LikeRepository.count_post_likes(
            db,
            post_id
        )

        return ToggleLikeResponse(
            liked=True,
            total_likes=total,
            message="Post liked successfully"
        )

    @staticmethod
    async def get_like_status(
        db: AsyncSession,
        post_id: int,
        current_user: User
    ):
        liked = await LikeRepository.is_liked(
            db,
            current_user.id,
            post_id
        )
        total = await LikeRepository.count_post_likes(
            db,
            post_id
        )

        return LikeStatusResponse(
            liked=liked,
            total_likes=total
        )
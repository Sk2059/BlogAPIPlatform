from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.models.user import User

from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository

from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
)

class CommentService:
    @staticmethod
    async def create_comment(
        db: AsyncSession,
        post_id: int,
        data: CommentCreate,
        current_user: User
    ):
        post = await PostRepository.get_by_id(
            db,
            post_id
        )
        if post is None:

            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )

        comment = Comment(
            content=data.content,
            user_id=current_user.id,
            post_id=post.id
        )
        return await CommentRepository.create(
            db,
            comment
        )

    @staticmethod
    async def reply_to_comment(
        db: AsyncSession,
        parent_id: int,
        data: CommentCreate,
        current_user: User
    ):
        parent = await CommentRepository.get_by_id(
            db,
            parent_id
        )
        if parent is None:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        reply = Comment(
            content=data.content,
            user_id=current_user.id,
            post_id=parent.post_id,
            parent_id=parent.id
        )
        return await CommentRepository.create(
            db,
            reply
        )

    @staticmethod
    async def get_comment(
        db: AsyncSession,
        comment_id: int
    ):
        comment = await CommentRepository.get_by_id(
            db,
            comment_id
        )
        if comment is None:

            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        return comment

    @staticmethod
    def verify_owner(
        comment: Comment,
        current_user: User
    ):

        if comment.user_id != current_user.id:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="You do not have permission to modify this comment."

            )

    @staticmethod
    async def update_comment(
        db: AsyncSession,
        comment_id: int,
        data: CommentUpdate,
        current_user: User
    ):
        comment = await CommentService.get_comment(
            db,
            comment_id
        )
        CommentService.verify_owner(
            comment,
            current_user
        )
        updates = data.model_dump(
            exclude_unset=True
        )
        for key, value in updates.items():
            setattr(comment, key, value)

        return await CommentRepository.update(
            db,
            comment
        )

    @staticmethod
    async def delete_comment(
        db: AsyncSession,
        comment_id: int,
        current_user: User
    ):
        comment = await CommentService.get_comment(
            db,
            comment_id
        )
        CommentService.verify_owner(
            comment,
            current_user
        )
        await CommentRepository.delete(
            db,
            comment
        )

    @staticmethod
    async def get_post_comments(
        db: AsyncSession,
        post_id: int
    ):
        post = await PostRepository.get_by_id(
            db,
            post_id
        )
        if post is None:
            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )
        return await CommentRepository.get_post_comments(
            db,
            post_id
        )

    
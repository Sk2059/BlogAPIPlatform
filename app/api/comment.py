from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentListResponse,
)
from app.services.comment_service import CommentService

router = APIRouter(
    prefix="",
    tags=["Comments"]
)

@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    post_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await CommentService.create_comment(
        db=db,
        post_id=post_id,
        data=data,
        current_user=current_user
    )

@router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentListResponse]
)
async def get_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await CommentService.get_post_comments(
        db,
        post_id
    )

@router.post(
    "/comments/{comment_id}/reply",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
async def reply_comment(
    comment_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await CommentService.reply_to_comment(
        db=db,
        parent_id=comment_id,
        data=data,
        current_user=current_user
    )

@router.patch(
    "/comments/{comment_id}",
    response_model=CommentResponse
)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await CommentService.update_comment(
        db=db,
        comment_id=comment_id,
        data=data,
        current_user=current_user
    )

@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    await CommentService.delete_comment(
        db=db,
        comment_id=comment_id,
        current_user=current_user
    )

    
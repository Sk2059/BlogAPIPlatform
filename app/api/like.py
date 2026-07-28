from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user

from app.models.user import User

from app.services.like_service import LikeService

from app.schemas.like import (
    LikeResponse,
    ToggleLikeResponse,
    LikeStatusResponse
)

router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)

@router.post(
    "/{post_id}/like",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED
)
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await LikeService.like_post(
        db=db,
        post_id=post_id,
        current_user=current_user
    )

@router.delete(
    "/{post_id}/like"
)
async def unlike_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await LikeService.unlike_post(
        db=db,
        post_id=post_id,
        current_user=current_user
    )

@router.post(
    "/{post_id}/toggle-like",
    response_model=ToggleLikeResponse
)
async def toggle_like(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await LikeService.toggle_like(
        db=db,
        post_id=post_id,
        current_user=current_user
    )

@router.get(
    "/{post_id}/like-status",
    response_model=LikeStatusResponse
)
async def get_like_status(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await LikeService.get_like_status(
        db=db,
        post_id=post_id,
        current_user=current_user
    )


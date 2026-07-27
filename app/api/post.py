from fastapi import  APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostListResponse,
    PostStatusUpdate
)
from app.services.post_service import PostService

router = APIRouter( prefix="/posts", tags=["Posts"])

@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await PostService.create_post(
        db,
        data,
        current_user
    )


@router.get(
    "",
    response_model=list[PostListResponse]
)
async def get_posts(
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)

):
    if search:
        return await PostService.search_posts(
            db,
            search,
            skip,
            limit
        )

    return await PostService.list_posts(
        db,
        skip,
        limit
    )

@router.get(
    "/me",
    response_model=list[PostListResponse]
)
async def my_posts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await PostService.my_posts(
        db,
        current_user,
        skip,
        limit
    )

@router.get(
    "/{slug}",
    response_model=PostResponse
)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db)
):

    return await PostService.get_post_by_slug(
        db,
        slug
    )


@router.patch(
    "/{post_id}",
    response_model=PostResponse
)
async def update_post(
    post_id: int,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await PostService.update_post(
        db,
        post_id,
        data,
        current_user
    )

@router.patch(
    "/{post_id}/status",
    response_model=PostResponse
)
async def update_status(
    post_id: int,
    status_data: PostStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await PostService.update_status(
        db,
        post_id,
        status_data,
        current_user
    )

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    await PostService.delete_post(
        db,
        post_id,
        current_user
    )

    

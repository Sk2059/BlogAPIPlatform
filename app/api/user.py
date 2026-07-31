from typing import List
from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserResponse,
    UserProfileResponse,
    UserProfileUpdate
)

from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_my_profile(
        current_user:User = Depends(get_current_user)
):
    return await UserService.get_my_profile(
        current_user
    )


@router.patch(
    "/me",
    response_model=UserResponse
)
async def update_profile(
    profile: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await UserService.update_profile(
        db=db,
        current_user=current_user,
        profile=profile
    )

@router.get(
    "/{username}",
    response_model=UserProfileResponse
)
async def get_public_profile(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    return await UserService.get_my_pubic_profile(
        db,
        username
    )
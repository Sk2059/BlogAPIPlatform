from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user  import UserProfileUpdate
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    async def get_my_profile(
            current_user=User
    ) -> User:
        return current_user

    

    @staticmethod
    async def get_my_prubic_profile(
        db:AsyncSession,
        username:str
    )-> User:

        user = await UserRepository.get_by_username(
            db,
            username
        )

        if user is None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return user

    

    @staticmethod
    async def update_profile(
        db:AsyncSession,
        current_user:User,
        profile:UserProfileUpdate
    ) -> User:
        
        data=profile.model_dump(
            exclude_unset=True
        )

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update."
            )

        if "full_name" in data:

            data["full_name"] = data["full_name"].strip()

            if not data["full_name"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Full name cannot be empty."
                )

        
        if "bio" in data:
            data["bio"] = data["bio"].strip()

        if "location" in data:
            data["location"] = data["location"].strip()

        if "website" in data and data["website"]:
            data["website"] = str(data["website"])

        if "avatar_url" in data and data["avatar_url"]:
            data["avatar_url"] = str(data["avatar_url"])

        return await UserRepository.update_profile(
        db,
        current_user,
        data
        )

    @staticmethod
    async def search_users(
        db: AsyncSession,
        query: str
    ):

        query = query.strip()

        if not query:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query cannot be empty."
            )

        if len(query) < 2:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query must contain at least 2 characters."
            )

        return await UserRepository.search_users(
            db,
            query
        )
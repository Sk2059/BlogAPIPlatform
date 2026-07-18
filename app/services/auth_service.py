from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password,verify_password
from app.core.jwt import create_access_token,create_refresh_token
from app.schemas.auth import LoginRequest , TokenResponse

class AuthService:

    @staticmethod
    async def register_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:

        existing_email = await (
            UserRepository.get_by_email(
                db,
                user_data.email
            )
        )

        if existing_email:
            raise ValueError(
                "Email already registered"
            )

        existing_username = await (
            UserRepository.get_by_username(
                db,
                user_data.username
            )
        )

        if existing_username:
            raise ValueError(
                "Username already exists"
            )

        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hash_password(
                user_data.password
            )
        )

        return await UserRepository.create(
            db,
            user
        )
    
    @staticmethod
    async def login(
        db:AsyncSession,
        credentials:LoginRequest,
    )-> TokenResponse:
        user = await ( UserRepository.get_by_email(
            db,
            credentials.email
            )
        )

        if not user :
            raise ValueError(
                "Invalid credentials"
            )
        
        if not verify_password(
            credentials.password,
            user.password_hash
        ):
            raise ValueError(
                "invalid credentials"
            )
        
        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = create_refresh_token(
            str(user.id)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
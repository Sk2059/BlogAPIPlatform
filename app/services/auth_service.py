from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timezone,timedelta

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password,verify_password
from app.core.jwt import create_access_token,create_refresh_token,decode_token
from app.schemas.auth import LoginRequest , TokenResponse , RefreshRequest
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.core.config import settings

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

        refresh = RefreshToken(
            user_id = user.id,
            token = refresh_token,
            expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS 
            )
        )
        await RefreshTokenRepository.create(
            db,
            refresh
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    @staticmethod
    async def refresh_access_token(
            db:AsyncSession,
            request:RefreshRequest
    ):
        stored_token = await (
            RefreshTokenRepository.get_by_token(
                db,
                request.refresh_token
            )
        )

        if not stored_token:
            raise ValueError("invalid refresh token")
        
        if stored_token.revoked:
            raise ValueError("Refresh token revoked")

        payload = decode_token(request.refresh_token)

        if payload is None:
            raise ValueError("Invalid token")
        
        user_id = payload["sub"]

        access = create_access_token(user_id)

        return {
        "access_token": access
        }
    
    @staticmethod
    async def logout(
        db:AsyncSession,
        refresh_token:str
    ):
        await RefreshTokenRepository.revoke(
            db,
            refresh_token
        )

        return {
            "logout successful"
        }
    
    @staticmethod
    async def logout_everywhere(
        db:AsyncSession,
        user_id:int
    ):
        await RefreshTokenRepository.revoke_all_user_token(
            db,
            user_id
        )

        return {
            "lout from all devices succeefull"
        }
        
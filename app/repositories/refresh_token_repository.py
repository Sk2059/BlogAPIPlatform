from sqlalchemy import select , update 

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    @staticmethod
    async def create(
        db:AsyncSession,
        refresh_token:RefreshToken
    ):
        db.add(refresh_token)
        await db.commit()
        await db.refresh(refresh_token)
        return refresh_token
    
    @staticmethod
    async def get_by_token(
        db:AsyncSession,
        token:str
    ):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def revoke(
        db:AsyncSession,
        token:str
    ):
        await db.execute(
            update(RefreshToken).where(
                RefreshToken.token == token
            ).values(revoked=True)
        )
        await db.commit()

    @staticmethod
    async def revoke_all_user_token(
        db: AsyncSession,
        user_id: int
    ):
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(revoked=True)
        )
        await db.commit()
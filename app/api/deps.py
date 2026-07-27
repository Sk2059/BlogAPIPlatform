from fastapi import Depends , HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.core.jwt import decode_token

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    payload = decode_token(token)

    if payload is None :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="invalid access token"
        )

    user_id = int(payload["sub"])

    user = await UserRepository.get_by_id(
        db,
        user_id
    )
    if user is None:
        raise HTTPException(
            status_code= 404,
            detail= "user not found"
        )    
    return user 
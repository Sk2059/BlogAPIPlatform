from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate ,UserResponse
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest,TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    try:
        user = await (
            AuthService.register_user(
                db,
                user_data
            )
        )

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    credentials : LoginRequest,
    db: AsyncSession = Depends(get_db)
    
):
    try:
        return await (
            AuthService.login(
                db,
                credentials
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
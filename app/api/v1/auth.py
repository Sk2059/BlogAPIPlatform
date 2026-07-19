from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate ,UserResponse
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest,TokenResponse,LogoutAllRequest
from app.schemas.auth import RefreshRequest


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
    
@router.post(
  "/refresh"
)
async def refresh_token(
    request: RefreshRequest,
    db: AsyncSession= Depends(get_db)
):
    try:
          return await AuthService.refresh_access_token(
               db,
               request
          )
    except ValueError as e:
         raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.post(
    "/logout"
)
async def logout(
    request:RefreshRequest,
    db:AsyncSession = Depends(get_db)
):
    await AuthService.logout(
        db,
        request.refresh_token
    )
    return {
        "message": "Successfully logged out."
    }

@router.post(
    "/logoutAll"
)
async def logoutAll(
    request: LogoutAllRequest,
    db:AsyncSession = Depends(get_db)
):
    await AuthService.logout_everywhere(
        db,
        request.user_id
    )
    return {
        "message": "Successfully logged out from everwhere."
    }
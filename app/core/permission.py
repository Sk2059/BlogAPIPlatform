from fastapi import Depends,HTTPException,status

from app.api.deps import get_current_user
from app.models.user import User
from app.models.enums import UserRole

def require_roles(*allowed_roles:UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action."
            )

        return current_user

    return role_checker
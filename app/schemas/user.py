from datetime import datetime 
from pydantic import BaseModel , EmailStr , ConfigDict,HttpUrl,Field

from app.models.enums import UserRole

class UserBase(BaseModel):
    email:EmailStr
    username : str

class UserCreate(UserBase):
    password:str

class UserResponse(BaseModel):

    id: int
    email: EmailStr
    username: str
    role: UserRole
    is_varified: bool
    full_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    website: str | None = None
    location: str | None = None
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class UserProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        max_length=100
    )

    bio: str | None = Field(
        default=None,
        max_length=500
    )

    avatar_url: HttpUrl | None = None

    website: HttpUrl | None = None

    location: str | None = Field(
        default=None,
        max_length=100
    )

class UserProfileResponse(BaseModel):

    username: str

    full_name: str | None = None

    bio: str | None = None

    avatar_url: str | None = None

    website: str | None = None

    location: str | None = None

    role: UserRole

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

    
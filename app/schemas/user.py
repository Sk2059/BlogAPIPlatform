from datetime import datetime 
from pydantic import BaseModel , EmailStr

from app.models.user import UserRole

class UserBase(BaseModel):
    email:EmailStr
    username : str

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id :int 
    role : UserRole
    is_varified : bool
    created_at : datetime

    model_config ={
        "from_attributes": True    
        }
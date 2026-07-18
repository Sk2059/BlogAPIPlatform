from datetime import datetime , timezone
from enum import Enum 

from sqlalchemy import String,Boolean,DateTime,Enum as SQLEnum
from sqlalchemy.orm import mapped_column,Mapped
from app.db.base_class import Base

class UserRole(str,Enum):
    USER = "USER"
    AUTHOR = "AUTHOR"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
        )
    
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False, 
        index=True
    )

    password_hash: Mapped[str]=mapped_column(
        String,
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    is_varified: Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime]=mapped_column(
         DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
    )
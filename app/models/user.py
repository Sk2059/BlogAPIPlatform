from datetime import datetime , timezone
from enum import Enum 

from sqlalchemy import String,Boolean,DateTime,Enum as SQLEnum
from sqlalchemy.orm import mapped_column,Mapped,relationship
from app.db.base_class import Base
from app.models.enums import UserRole

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

    full_name: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True
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

    bio: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    posts: Mapped[list["Post"]] = relationship(
    back_populates="author",
    cascade="all, delete-orphan",
    )
    
    comments = relationship(
    "Comment",
    back_populates="author",
    cascade="all, delete-orphan"
)

    location: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
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
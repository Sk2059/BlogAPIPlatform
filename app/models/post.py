from datetime import datetime , timezone
from enum import Enum
from app.models.user import User
from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
    DateTime
)
from sqlalchemy.orm import(
    relationship,
    mapped_column,
    Mapped
)
from app.db.base_class import Base

class PostStatus(str,Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)

    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(PostStatus),
        default=PostStatus.DRAFT,
        nullable=False,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        back_populates="posts"
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
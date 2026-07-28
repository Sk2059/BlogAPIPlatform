from datetime import datetime, timezone
from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from app.db.base import Base

class Like(Base):

    __tablename__ = "likes"

    __table_args__ = (

        UniqueConstraint(

            "user_id",

            "post_id",

            name="uq_user_post_like"

        ),

    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "User",
        back_populates="likes"
    )

    post = relationship(
        "Post",
        back_populates="likes"
    )

    
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.post import PostStatus


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    excerpt: Optional[str] = Field(default=None, max_length=500)
    cover_image: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, min_length=1)
    excerpt: Optional[str] = Field(default=None, max_length=500)
    cover_image: Optional[str] = None


class PostStatusUpdate(BaseModel):
    status: PostStatus


class PostResponse(PostBase):
    id: int
    slug: str
    status: PostStatus
    author_id: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True
    )


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    cover_image: Optional[str]
    status: PostStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
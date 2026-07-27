from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000,
        examples=["Great article!"]
    )

class CommentUpdate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000
    )

class CommentAuthor(BaseModel):
    id: int
    username: str
    avatar_url: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )

class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    parent_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class CommentListResponse(BaseModel):
    id: int
    content: str
    parent_id: int | None
    created_at: datetime
    updated_at: datetime
    author: CommentAuthor
    replies: list["CommentListResponse"] = []

    model_config = ConfigDict(
        from_attributes=True
    )

CommentListResponse.model_rebuild()
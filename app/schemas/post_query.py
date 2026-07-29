from typing import Literal
from pydantic import BaseModel, Field

class PostQuery(BaseModel):
    page: int = Field(
        default=1,
        ge=1
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100
    )
    sort: Literal[
        "newest",
        "oldest",
        "popular"
    ] = "newest"
    published: bool | None = None
    author: str | None = None
    search: str | None = None
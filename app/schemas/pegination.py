from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginationResponse(BaseModel, Generic[T]):

    page: int

    limit: int

    total_items: int

    total_pages: int

    has_next: bool

    has_previous: bool

    items: list[T]
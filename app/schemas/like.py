from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class LikeStatusResponse(BaseModel):
    liked: bool
    total_likes: int

class ToggleLikeResponse(BaseModel):
    liked: bool
    total_likes: int
    message: str


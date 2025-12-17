from pydantic import BaseModel
from typing import Optional


class FavoriteResponse(BaseModel):
    """Schema for favorite response"""
    id: int
    movie_id: int
    user_id: int
    added_at: Optional[str] = None

    class Config:
        from_attributes = True

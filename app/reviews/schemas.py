from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    """Schema for creating a review"""
    text: str
    rating: Optional[int] = None


class ReviewResponse(BaseModel):
    """Schema for review response"""
    id: int
    movie_id: int
    user_id: int
    text: str
    rating: Optional[int] = None
    approved: bool
    username: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

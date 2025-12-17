from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    """Schema for creating a review"""
    text: str
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    """Schema for updating a review"""
    text: Optional[str] = None
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    """Schema for review response"""
    id: int
    movie_id: int
    user_id: int
    text: str
    rating: Optional[int]
    approved: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

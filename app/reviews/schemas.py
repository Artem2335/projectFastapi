from pydantic import BaseModel
from typing import Optional


class ReviewCreate(BaseModel):
    text: str
    rating: Optional[int] = None

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    user_id: int
    text: str
    rating: Optional[int]
    approved: bool
    username: Optional[str] = None

    class Config:
        from_attributes = True

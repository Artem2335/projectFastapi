from pydantic import BaseModel
from typing import Optional


class FavoriteResponse(BaseModel):
    id: int
    movie_id: int
    user_id: int

    class Config:
        from_attributes = True


class MovieInFavoritesResponse(BaseModel):
    """Response with favorite movie details"""
    id: int
    title: str
    description: Optional[str] = None
    genre: str
    year: int
    poster_url: Optional[str] = None

    class Config:
        from_attributes = True

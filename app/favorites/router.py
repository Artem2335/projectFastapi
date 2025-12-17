from fastapi import APIRouter, HTTPException
from typing import List
from app import db

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("/users/{user_id}")
def get_user_favorites(user_id: int):
    """
    Get user's favorite movies
    
    Parameters:
    - user_id: ID of the user
    """
    favorites = db.get_user_favorites(user_id)
    return favorites


@router.post("/movies/{movie_id}")
def add_to_favorites(movie_id: int, user_id: int):
    """
    Add a movie to user's favorites
    
    Parameters:
    - movie_id: ID of the movie to add to favorites
    - user_id: ID of the user
    """
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/movies/{movie_id}")
def remove_from_favorites(movie_id: int, user_id: int):
    """
    Remove a movie from user's favorites
    
    Parameters:
    - movie_id: ID of the movie to remove from favorites
    - user_id: ID of the user
    """
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/movies/{movie_id}/users/{user_id}")
def check_favorite(movie_id: int, user_id: int):
    """
    Check if a movie is in user's favorites
    
    Parameters:
    - movie_id: ID of the movie
    - user_id: ID of the user
    """
    is_fav = db.is_favorite(movie_id, user_id)
    return {"is_favorite": is_fav}

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from app import db

router = APIRouter(prefix="/api/movies", tags=["movies"])

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    year: int
    poster_url: Optional[str] = None

# ========== MOVIES ==========

@router.get("/")
def get_movies(genre: Optional[str] = Query(None), sort: str = Query("popular")):
    """Get all movies with optional filtering and sorting"""
    movies = db.get_all_movies()
    
    if genre and genre != "all":
        movies = [m for m in movies if m['genre'] == genre]
    
    if sort == "title":
        movies = sorted(movies, key=lambda x: x['title'])
    elif sort == "year":
        movies = sorted(movies, key=lambda x: x['year'], reverse=True)
    
    return movies

@router.get("/stats")
def get_stats():
    """Get overall site statistics"""
    movies = db.get_all_movies()
    movies_count = len(movies)
    
    # Count all reviews
    reviews_count = 0
    for movie in movies:
        reviews = db.get_movie_reviews(movie['id'], approved_only=False)
        reviews_count += len(reviews)
    
    return {
        "movies_count": movies_count,
        "reviews_count": reviews_count
    }

@router.get("/{movie_id}")
def get_movie(movie_id: int):
    """Get a single movie by ID"""
    movie = db.get_movie_by_id(movie_id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

@router.post("/")
def create_movie(data: MovieCreate):
    """Create a new movie (admin only)"""
    movie = db.create_movie(
        title=data.title,
        description=data.description,
        genre=data.genre,
        year=data.year,
        poster_url=data.poster_url
    )
    return movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    """
    Delete a movie and all related data (admin only)
    
    This will delete:
    - Movie entry
    - All reviews for the movie
    - All ratings for the movie
    - All favorites containing this movie
    """
    movie = db.get_movie_by_id(movie_id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    conn = db.get_db()
    cursor = conn.cursor()
    
    try:
        # Delete related data (cascading)
        # Delete reviews
        cursor.execute("DELETE FROM reviews WHERE movie_id = ?", (movie_id,))
        # Delete ratings
        cursor.execute("DELETE FROM ratings WHERE movie_id = ?", (movie_id,))
        # Delete favorites
        cursor.execute("DELETE FROM favorites WHERE movie_id = ?", (movie_id,))
        # Delete movie
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        
        conn.commit()
        return {
            "status": "deleted",
            "message": f"Movie '{movie['title']}' and all related data have been deleted",
            "movie_id": movie_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting movie: {str(e)}")
    finally:
        conn.close()

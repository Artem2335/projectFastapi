from app.movies.models import Movie, Review, Rating, Favorite
from typing import Optional, List
from sqlalchemy.orm import Session


class MovieDAO:
    """Data Access Object for Movie operations"""
    
    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int) -> Optional[Movie]:
        """Get movie by ID"""
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_all_movies(db: Session, skip: int = 0, limit: int = 100):
        """Get all movies with pagination"""
        return db.query(Movie).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_movie(db: Session, title: str, description: str, genre: str, 
                    year: int, poster_url: str = None) -> Movie:
        """Create a new movie"""
        movie = Movie(
            title=title,
            description=description,
            genre=genre,
            year=year,
            poster_url=poster_url
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int) -> bool:
        """Delete movie and all related data (cascade)"""
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return False
        
        db.delete(movie)
        db.commit()
        return True
    
    @staticmethod
    def get_movies_by_genre(db: Session, genre: str, skip: int = 0, limit: int = 100):
        """Get movies by genre"""
        return db.query(Movie).filter(Movie.genre == genre).offset(skip).limit(limit).all()

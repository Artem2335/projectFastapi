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


class ReviewDAO:
    """Data Access Object for Review operations"""
    
    @staticmethod
    def get_review_by_id(db: Session, review_id: int) -> Optional[Review]:
        """Get review by ID"""
        return db.query(Review).filter(Review.id == review_id).first()
    
    @staticmethod
    def get_movie_reviews(db: Session, movie_id: int, approved_only: bool = True):
        """Get reviews for a movie"""
        query = db.query(Review).filter(Review.movie_id == movie_id)
        if approved_only:
            query = query.filter(Review.approved == True)
        return query.all()


class RatingDAO:
    """Data Access Object for Rating operations"""
    
    @staticmethod
    def get_rating_by_id(db: Session, rating_id: int) -> Optional[Rating]:
        """Get rating by ID"""
        return db.query(Rating).filter(Rating.id == rating_id).first()
    
    @staticmethod
    def get_movie_ratings(db: Session, movie_id: int):
        """Get all ratings for a movie"""
        return db.query(Rating).filter(Rating.movie_id == movie_id).all()


class FavoriteDAO:
    """Data Access Object for Favorite operations"""
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: int):
        """Get user's favorite movies"""
        return db.query(Favorite).filter(Favorite.user_id == user_id).all()
    
    @staticmethod
    def is_favorite(db: Session, movie_id: int, user_id: int) -> bool:
        """Check if movie is in user's favorites"""
        return db.query(Favorite).filter(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        ).first() is not None

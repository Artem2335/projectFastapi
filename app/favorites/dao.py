from app.movies.models import Favorite
from typing import Optional, List
from sqlalchemy.orm import Session


class FavoriteDAO:
    """Data Access Object for Favorite operations"""
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """Get user's favorite movies"""
        return db.query(Favorite).filter(Favorite.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def is_favorite(db: Session, movie_id: int, user_id: int) -> bool:
        """Check if movie is in user's favorites"""
        return db.query(Favorite).filter(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        ).first() is not None
    
    @staticmethod
    def add_favorite(db: Session, movie_id: int, user_id: int) -> Optional[Favorite]:
        """Add movie to user's favorites"""
        # Check if already exists
        existing = db.query(Favorite).filter(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        ).first()
        
        if existing:
            return None  # Already in favorites
        
        favorite = Favorite(
            movie_id=movie_id,
            user_id=user_id
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    
    @staticmethod
    def remove_favorite(db: Session, movie_id: int, user_id: int) -> bool:
        """Remove movie from user's favorites"""
        favorite = db.query(Favorite).filter(
            Favorite.movie_id == movie_id,
            Favorite.user_id == user_id
        ).first()
        
        if not favorite:
            return False
        
        db.delete(favorite)
        db.commit()
        return True
    
    @staticmethod
    def get_favorite_by_id(db: Session, favorite_id: int) -> Optional[Favorite]:
        """Get favorite by ID"""
        return db.query(Favorite).filter(Favorite.id == favorite_id).first()

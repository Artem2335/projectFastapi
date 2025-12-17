from app.movies.models import Review
from typing import Optional, List
from sqlalchemy.orm import Session


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
    
    @staticmethod
    def create_review(db: Session, movie_id: int, user_id: int, text: str, rating: int = None) -> Review:
        """Create a new review"""
        review = Review(
            movie_id=movie_id,
            user_id=user_id,
            text=text,
            rating=rating,
            approved=False
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    
    @staticmethod
    def approve_review(db: Session, review_id: int) -> bool:
        """Approve a review"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return False
        
        review.approved = True
        db.commit()
        return True
    
    @staticmethod
    def delete_review(db: Session, review_id: int) -> bool:
        """Delete a review"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return False
        
        db.delete(review)
        db.commit()
        return True
    
    @staticmethod
    def get_user_reviews(db: Session, user_id: int, skip: int = 0, limit: int = 10):
        """Get all reviews by a user"""
        return db.query(Review).filter(Review.user_id == user_id).offset(skip).limit(limit).all()

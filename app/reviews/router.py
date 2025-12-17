from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app import db
from app.reviews.schemas import ReviewCreate

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    text: str
    rating: int = None


@router.post("/movie/{movie_id}")
def create_review(movie_id: int, data: ReviewCreate, user_id: int):
    """
    Create a review for a movie
    
    Parameters:
    - movie_id: ID of the movie
    - user_id: ID of the user (from auth)
    - data: ReviewCreate schema with text and optional rating
    """
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    review = db.create_review(
        movie_id=movie_id,
        user_id=user_id,
        text=data.text,
        rating=data.rating
    )
    return review


@router.get("/movie/{movie_id}")
def get_movie_reviews(movie_id: int, approved_only: bool = Query(True)):
    """
    Get reviews for a specific movie
    
    Parameters:
    - movie_id: ID of the movie
    - approved_only: Filter to show only approved reviews (default: True)
    """
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews


@router.get("/{review_id}")
def get_review(review_id: int):
    """Get a single review by ID"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}/approve")
def approve_review(review_id: int):
    """
    Approve a review (moderator only)
    
    Changes review status to approved so it appears publicly
    """
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.approve_review(review_id)
    return {"status": "approved", "review_id": review_id}


@router.delete("/{review_id}")
def delete_review(review_id: int):
    """
    Delete a review
    
    Can be done by:
    - Owner of the review
    - Moderator
    - Admin
    """
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete_review(review_id)
    return {"status": "deleted", "review_id": review_id}

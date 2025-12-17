from fastapi import APIRouter, HTTPException, Query
from app import db
from app.reviews.schemas import ReviewCreate

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

# ========== REVIEWS ==========

@router.post("/movies/{movie_id}")
def create_review(movie_id: int, data: ReviewCreate, user_id: int):
    """
    Create a review for a movie
    
    - movie_id: ID of the movie to review
    - user_id: ID of the user creating the review
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


@router.get("/movies/{movie_id}")
def get_reviews(movie_id: int, approved_only: bool = Query(True)):
    """
    Get reviews for a movie
    
    - movie_id: ID of the movie
    - approved_only: If True, only return approved reviews (default: True)
    """
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews


@router.put("/{review_id}/approve")
def approve_review(review_id: int):
    """
    Approve a review (moderator only)
    
    - review_id: ID of the review to approve
    """
    result = db.approve_review(review_id)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"status": "approved", "review_id": review_id}


@router.delete("/{review_id}")
def delete_review(review_id: int):
    """
    Delete a review
    
    - review_id: ID of the review to delete
    """
    result = db.delete_review(review_id)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"status": "deleted", "review_id": review_id}

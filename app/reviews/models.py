from sqlalchemy import text, String, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.movies.models import Movie
    from app.users.models import User


class Review(Base):
    """Review model - user reviews for movies"""
    __tablename__ = "reviews"
    
    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)  # рейтинг в рецензии (1-5)
    approved: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews", foreign_keys=[movie_id])
    user: Mapped["User"] = relationship("User", back_populates="reviews", foreign_keys=[user_id])

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, movie_id={self.movie_id})"


class Rating(Base):
    """Rating model - user ratings for movies"""
    __tablename__ = "ratings"
    
    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)  # рейтинг в звездочках (1-5)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="ratings", foreign_keys=[movie_id])
    user: Mapped["User"] = relationship("User", back_populates="ratings", foreign_keys=[user_id])

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, movie_id={self.movie_id})"

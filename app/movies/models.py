from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.reviews.models import Review, Rating
    from app.favorites.models import Favorite


class Movie(Base):
    """Movie model"""
    __tablename__ = "movies"
    
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="movie", cascade="all, delete-orphan", foreign_keys="Review.movie_id")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="movie", cascade="all, delete-orphan", foreign_keys="Rating.movie_id")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan", foreign_keys="Favorite.movie_id")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"

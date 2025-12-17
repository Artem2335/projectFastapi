"""SQLAlchemy models for the application."""
from typing import Annotated
from datetime import datetime

from sqlalchemy import ForeignKey, func, String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, created_at, updated_at, str_uniq


class User(Base):
    """User model."""
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    password: Mapped[str]
    username: Mapped[str_uniq]
    is_user: Mapped[bool] = mapped_column(default=True)
    is_moderator: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Relationships
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Review.user_id"
    )
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Rating.user_id"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Favorite.user_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Movie(Base):
    """Movie model."""
    __tablename__ = "movies"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Relationships
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
        foreign_keys="Review.movie_id"
    )
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
        foreign_keys="Rating.movie_id"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
        foreign_keys="Favorite.movie_id"
    )

    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title={self.title}, year={self.year})>"


class Review(Base):
    """Review model."""
    __tablename__ = "reviews"

    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)  # 1-5 stars
    approved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Relationships
    movie: Mapped["Movie"] = relationship(
        back_populates="reviews",
        foreign_keys=[movie_id]
    )
    user: Mapped["User"] = relationship(
        back_populates="reviews",
        foreign_keys=[user_id]
    )

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id}, rating={self.rating})>"


class Rating(Base):
    """Rating model for aggregated movie ratings."""
    __tablename__ = "ratings"

    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)  # 0-5 stars
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Relationships
    movie: Mapped["Movie"] = relationship(
        back_populates="ratings",
        foreign_keys=[movie_id]
    )
    user: Mapped["User"] = relationship(
        back_populates="ratings",
        foreign_keys=[user_id]
    )

    def __repr__(self) -> str:
        return f"<Rating(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id}, value={self.value})>"


class Favorite(Base):
    """Favorite model for user's favorite movies."""
    __tablename__ = "favorites"

    id: Mapped[int_pk]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Relationships
    movie: Mapped["Movie"] = relationship(
        back_populates="favorites",
        foreign_keys=[movie_id]
    )
    user: Mapped["User"] = relationship(
        back_populates="favorites",
        foreign_keys=[user_id]
    )

    def __repr__(self) -> str:
        return f"<Favorite(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id})>"

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.reviews.models import Review, Rating
    from app.favorites.models import Favorite


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    password: Mapped[str]
    username: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True, server_default="1", nullable=False)
    is_moderator: Mapped[bool] = mapped_column(default=False, server_default="0", nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0", nullable=False)

    # Relationships
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan", foreign_keys="Review.user_id")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="user", cascade="all, delete-orphan", foreign_keys="Rating.user_id")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="user", cascade="all, delete-orphan", foreign_keys="Favorite.user_id")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

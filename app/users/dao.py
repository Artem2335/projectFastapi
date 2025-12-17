from app.users.models import User
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session


class UserDAO:
    """Data Access Object for User operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, username: str) -> User:
        """Create a new user"""
        user = User(
            email=email,
            password=password,
            username=username,
            is_user=True,
            is_moderator=False,
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """Update user profile"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Update only provided fields
        for field, value in update_data.items():
            if value is not None and hasattr(user, field):
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user and all related data (cascade)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 10):
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

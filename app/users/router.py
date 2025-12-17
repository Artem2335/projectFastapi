from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from app import db
from app.security import verify_password
import json

router = APIRouter(prefix="/api/users", tags=["users"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None

@router.post("/register")
def register(data: UserRegister):
    """Register a new user"""
    # Check if user already exists
    existing = db.get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = db.create_user(data.email, data.password, data.username)
    return user

@router.post("/login")
def login(data: UserLogin):
    """Login user by username with secure password verification"""
    print(f"Login attempt with: {json.dumps({'username': data.username, 'password': '***'})}")
    
    # Get user by username
    user = db.get_user_by_username(data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password using bcrypt
    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user

@router.get("/me")
def get_current_user(user_id: int):
    """Get current user info"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    """
    Update user information
    
    Can update: email, password, username
    Only non-None fields will be updated
    Passwords are automatically hashed
    """
    # Check if user exists
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If email is being changed, check if it's already taken
    if data.email and data.email != user['email']:
        existing = db.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # If username is being changed, check if it's already taken
    if data.username and data.username != user['username']:
        existing = db.get_user_by_username(data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    # Update user
    updated_user = db.update_user(
        user_id,
        email=data.email,
        password=data.password,
        username=data.username
    )
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    """
    Delete user by ID
    
    This will also delete all user's related data:
    - Reviews
    - Ratings  
    - Favorites
    """
    # Check if user exists
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    success = db.delete_user(user_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return {"status": "deleted", "user_id": user_id}

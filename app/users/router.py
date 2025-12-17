from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app import db
from app.users.schemas import UserUpdate, UserResponse
from app.users.dao import UserDAO
from app.security import verify_password
from sqlalchemy.orm import Session
from app.database import get_db
import json

router = APIRouter(prefix="/api/users", tags=["users"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

# ========== CREATE ==========

@router.post("/register")
def register(data: UserRegister):
    """Register a new user with automatic password hashing"""
    # Check if user already exists
    existing = db.get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    existing_username = db.get_user_by_username(data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = db.create_user(data.email, data.password, data.username)
    return user

@router.post("/login")
def login(data: UserLogin):
    """
    Login user by username
    
    Password is automatically verified against the hashed password in database
    """
    print(f"Login attempt with: {json.dumps({'username': data.username, 'password': '***'})}")
    
    # Get user by username
    user = db.get_user_by_username(data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password using bcrypt
    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user

# ========== READ ==========

@router.get("/me")
def get_current_user(user_id: int):
    """Get current user info"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/{user_id}")
def get_user(user_id: int):
    """Get user by ID"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# ========== UPDATE ==========

@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    """
    Update user profile (email, username, password)
    
    Only provide fields you want to update:
    - email: new email address
    - username: new username
    - password: new password (will be automatically hashed)
    """
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email already exists (if changing email)
    if data.email and data.email != user['email']:
        existing_email = db.get_user_by_email(data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already in use")
    
    # Check if new username already exists (if changing username)
    if data.username and data.username != user['username']:
        existing_username = db.get_user_by_username(data.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Update user
    conn = db.get_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if data.email:
        updates.append("email = ?")
        params.append(data.email)
    
    if data.username:
        updates.append("username = ?")
        params.append(data.username)
    
    if data.password:
        # Hash password before storing
        from app.security import hash_password
        hashed_password = hash_password(data.password)
        updates.append("password = ?")
        params.append(hashed_password)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    params.append(user_id)
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
    # Return updated user
    updated_user = db.get_user_by_id(user_id)
    return updated_user

# ========== DELETE ==========

@router.delete("/{user_id}")
def delete_user(user_id: int):
    """
    Delete user account and all related data
    
    This will delete:
    - User profile
    - All user reviews
    - All user ratings
    - All user favorites
    """
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conn = db.get_db()
    cursor = conn.cursor()
    
    try:
        # Delete related data (cascading)
        # Delete reviews
        cursor.execute("DELETE FROM reviews WHERE user_id = ?", (user_id,))
        # Delete ratings
        cursor.execute("DELETE FROM ratings WHERE user_id = ?", (user_id,))
        # Delete favorites
        cursor.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        return {
            "status": "deleted",
            "message": f"User {user['username']} and all related data have been deleted",
            "user_id": user_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
    finally:
        conn.close()

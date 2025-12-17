# Refactoring Changes - Module Reorganization & Security

## Overview

This refactoring improves the project structure by:
1. Organizing Reviews and Favorites into separate modules
2. Removing Ratings endpoints (keeping data model for future use)
3. Implementing secure password hashing with bcrypt
4. Creating a security module for password management

---

## Changes Made

### 1. New Module Structure

#### Reviews Module (`app/reviews/`)
- **router.py**: Reviews endpoints (create, get, approve, delete)
- **dao.py**: ReviewDAO for database operations
- **schemas.py**: ReviewCreate and ReviewResponse schemas

**Endpoints:**
- `POST /api/reviews/movies/{movie_id}` - Create review
- `GET /api/reviews/movies/{movie_id}` - Get reviews for movie
- `PUT /api/reviews/{review_id}/approve` - Approve review (moderator)
- `DELETE /api/reviews/{review_id}` - Delete review

#### Favorites Module (`app/favorites/`)
- **router.py**: Favorites endpoints (add, remove, get)
- **dao.py**: FavoriteDAO for database operations
- **schemas.py**: Favorite response schemas

**Endpoints:**
- `GET /api/favorites/users/{user_id}` - Get user's favorites
- `POST /api/favorites/movies/{movie_id}` - Add to favorites
- `DELETE /api/favorites/movies/{movie_id}` - Remove from favorites
- `GET /api/favorites/movies/{movie_id}/users/{user_id}` - Check if favorite

### 2. Movies Module Cleanup

**Removed from `app/movies/router.py`:**
- `POST /api/movies/{movie_id}/ratings` - Create rating
- `GET /api/movies/{movie_id}/rating-stats` - Get rating statistics

**Removed from `app/movies/dao.py`:**
- `RatingDAO` class (ratings functionality removed)

**Kept in `app/movies/`:**
- Movie CRUD operations (create, read, delete)
- Stats endpoint

### 3. Security Module (`app/security.py`)

**Password Hashing Functions:**
- `hash_password(password: str) -> str` - Hash password using bcrypt
- `verify_password(plain_password: str, hashed_password: str) -> bool` - Verify password

**Configuration:**
- Using bcrypt with 12 rounds of salting (cost factor)
- Salt generated for each password

### 4. Database Layer Updates (`app/db.py`)

**New Functions:**
- `authenticate_user(username: str, password: str)` - Authenticate user with password verification
- `verify_user_password(user_id: int, password: str)` - Verify specific user password

**Updated Functions:**
- `create_user()` - Now automatically hashes password before storing
- `create_review()` - Automatically sets approved=False
- `approve_review()` - Set review as approved (moderator only)
- `delete_review()` - Delete review from database

### 5. Router Updates

#### Users Router (`app/users/router.py`)
- **Register endpoint**: Automatically hashes password
- **Login endpoint**: Now verifies password using bcrypt comparison
- **Update endpoint**: Hashes new password if provided
- **Delete endpoint**: Cascade deletes all user data

#### Movies Router (`app/movies/router.py`)
- **Cleaned up**: Only contains movie operations
- **No ratings endpoints**: Removed POST/GET rating endpoints

#### Main App (`app/main.py`)
- **New routers included**:
  ```python
  app.include_router(router_reviews)
  app.include_router(router_favorites)
  ```

---

## API Changes Summary

### Removed Endpoints
```
❌ POST /api/movies/{movie_id}/ratings
❌ GET /api/movies/{movie_id}/rating-stats
```

### Moved Endpoints
```
📍 Reviews (now under /api/reviews/):
   POST /api/reviews/movies/{movie_id}
   GET /api/reviews/movies/{movie_id}
   PUT /api/reviews/{review_id}/approve
   DELETE /api/reviews/{review_id}

📍 Favorites (now under /api/favorites/):
   GET /api/favorites/users/{user_id}
   POST /api/favorites/movies/{movie_id}
   DELETE /api/favorites/movies/{movie_id}
   GET /api/favorites/movies/{movie_id}/users/{user_id}
```

---

## Password Security

### Before
- Passwords stored in plain text
- Direct password comparison
- Security risk for user data

### After
- Passwords hashed with bcrypt
- 12 rounds of salting (industry standard)
- Secure comparison during authentication
- Each password gets unique salt

**Example:**
```python
# Registration
user = create_user("user@example.com", "password123", "username")
# Password is automatically hashed and stored

# Login
user = authenticate_user("username", "password123")
# Password is verified against hash
```

---

## Installation Requirements

**Added dependency:**
```
bcrypt>=4.0.0
```

**Update requirements.txt:**
```bash
pip install bcrypt
```

---

## Migration Notes

### For Existing Databases

If you have an existing database with plain text passwords, consider:

1. **Option 1: Rehash passwords**
   ```python
   # Script to rehash existing passwords
   from app.security import hash_password
   # Load and rehash each password
   ```

2. **Option 2: Reset all passwords**
   - Users need to reset passwords on next login
   - Old passwords become invalid

3. **Option 3: Start fresh**
   - Delete existing database
   - New database created with proper hashing

---

## Testing

### Registration
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "pass123", "username": "testuser"}'
```

### Login (with password verification)
```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "pass123"}'
```

### Create Review
```bash
curl -X POST http://localhost:8000/api/reviews/movies/1 \
  -H "Content-Type: application/json" \
  -d '{"text": "Great movie!", "rating": 4}' \
  -G -d "user_id=1"
```

### Add to Favorites
```bash
curl -X POST http://localhost:8000/api/favorites/movies/1 \
  -G -d "user_id=1"
```

---

## File Structure

```
app/
├── __init__.py
├── main.py                 # Updated with new routers
├── config.py
├── database.py
├── db.py                   # Updated with hashing
├── security.py            # 🆕 Password hashing utilities
├── users/
│   ├── __init__.py
│   ├── models.py
│   ├── router.py          # Updated for hashing
│   ├── schemas.py
│   └── dao.py
├── movies/
│   ├── __init__.py
│   ├── models.py
│   ├── router.py          # Cleaned up (no ratings)
│   ├── schemas.py
│   └── dao.py             # Cleaned up (no RatingDAO)
├── reviews/               # 🆕 New module
│   ├── __init__.py
│   ├── router.py
│   ├── schemas.py
│   └── dao.py
├── favorites/             # 🆕 New module
│   ├── __init__.py
│   ├── router.py
│   ├── schemas.py
│   └── dao.py
└── static/
```

---

## Benefits

✅ **Better Code Organization**
- Each feature has its own module
- Clear separation of concerns
- Easier to maintain and test

✅ **Enhanced Security**
- Passwords securely hashed
- Industry-standard bcrypt algorithm
- Protection against common attacks

✅ **Cleaner API**
- Logical endpoint organization
- Easier for frontend to consume
- RESTful structure

✅ **Scalability**
- Easy to add new modules
- Simple to extend functionality
- Clear patterns for future development

---

## Next Steps

1. ✅ Merge this PR
2. Update frontend to use new endpoints
3. Consider adding JWT authentication
4. Add request/response logging
5. Implement rate limiting
6. Add comprehensive tests

---

# Refactoring Guide: Modularization & Security

## Overview

This guide explains the architectural changes made to improve security, maintainability, and scalability.

---

## 🔐 Password Security Enhancement

### What Changed

**Before:**
- Passwords stored as plain text in database
- Direct string comparison for login
- Vulnerable to brute force attacks
- Database breach exposes all passwords

**After:**
- Passwords hashed with bcrypt (12 rounds)
- Secure password verification
- Each password has unique salt
- Industry-standard encryption

### Implementation

**New Module:** `app/security.py`

```python
from app.security import hash_password, verify_password

# Creating user - automatic hashing
user = db.create_user(
    email="user@example.com",
    password="mypassword",  # Will be hashed
    username="john_doe"
)

# Login - secure verification
if verify_password(provided_password, user['password']):
    # User authenticated successfully
    pass
```

### Installation

```bash
pip install bcrypt>=4.0.0
# Or
pip install -r requirements.txt
```

---

## 📁 Module Organization

### New Structure

```
app/
├── users/          # User management
├── movies/         # Movie CRUD only
├── reviews/        # Reviews (NEW)
├── favorites/      # Favorites (NEW)
└── security.py     # Password hashing (NEW)
```

### Benefits

✅ **Separation of Concerns**
- Each module handles one responsibility
- Easier to test individual modules
- Clear module boundaries

✅ **Maintainability**
- Find code related to reviews → go to `reviews/` module
- Find code related to favorites → go to `favorites/` module
- Clear organization reduces confusion

✅ **Scalability**
- Easy to add new modules
- Each module can be developed independently
- Supports team development

---

## 🔄 API Endpoint Changes

### Reviews Endpoints

**Old Endpoints:**
```
POST   /api/movies/{movie_id}/reviews
GET    /api/movies/{movie_id}/reviews
PUT    /api/movies/reviews/{review_id}/approve
DELETE /api/movies/reviews/{review_id}
```

**New Endpoints:**
```
POST   /api/reviews/movies/{movie_id}
GET    /api/reviews/movies/{movie_id}
PUT    /api/reviews/{review_id}/approve
DELETE /api/reviews/{review_id}
```

### Favorites Endpoints

**Old Endpoints:**
```
POST   /api/movies/{movie_id}/favorites
GET    /api/movies/user/{user_id}/favorites
DELETE /api/movies/{movie_id}/favorites
```

**New Endpoints:**
```
POST   /api/favorites/movies/{movie_id}
GET    /api/favorites/users/{user_id}
DELETE /api/favorites/movies/{movie_id}
GET    /api/favorites/movies/{movie_id}/users/{user_id}  # NEW: Check if favorite
```

### Ratings Endpoints

**Removed:**
```
POST   /api/movies/{movie_id}/ratings          ❌ REMOVED
GET    /api/movies/{movie_id}/rating-stats     ❌ REMOVED
```

**Note:** Rating data is preserved in database. These endpoints can be re-enabled in future if needed.

---

## 🔧 Migration Guide for Developers

### Frontend/Mobile App Migration

**Step 1: Update Review Endpoints**

```javascript
// OLD
fetch('/api/movies/1/reviews', { method: 'GET' })

// NEW
fetch('/api/reviews/movies/1', { method: 'GET' })
```

**Step 2: Update Favorites Endpoints**

```javascript
// OLD
fetch('/api/movies/1/favorites', { method: 'POST' })

// NEW
fetch('/api/favorites/movies/1', { method: 'POST' })
```

**Step 3: Remove Ratings Calls**

```javascript
// OLD
fetch('/api/movies/1/rating-stats', { method: 'GET' })  // Remove this

// NEW - No replacement
```

### Backend Integration

**Using New Modules:**

```python
from app.reviews.router import router as router_reviews
from app.favorites.router import router as router_favorites

app.include_router(router_reviews)
app.include_router(router_favorites)
```

---

## 🧪 Testing

### Test Password Hashing

```bash
# Register new user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "mypassword",
    "username": "testuser"
  }'

# Login with correct password
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "mypassword"
  }'

# Login with wrong password (should fail)
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "wrongpassword"
  }'
```

### Test New Review Endpoints

```bash
# Create review
curl -X POST http://localhost:8000/api/reviews/movies/1 \
  -H "Content-Type: application/json" \
  -G -d "user_id=1" \
  -d '{"text": "Great movie!", "rating": 5}'

# Get reviews
curl http://localhost:8000/api/reviews/movies/1

# Approve review
curl -X PUT http://localhost:8000/api/reviews/1/approve

# Delete review
curl -X DELETE http://localhost:8000/api/reviews/1
```

### Test New Favorites Endpoints

```bash
# Add to favorites
curl -X POST http://localhost:8000/api/favorites/movies/1 \
  -G -d "user_id=1"

# Get user favorites
curl http://localhost:8000/api/favorites/users/1

# Check if favorite
curl http://localhost:8000/api/favorites/movies/1/users/1

# Remove from favorites
curl -X DELETE http://localhost:8000/api/favorites/movies/1 \
  -G -d "user_id=1"
```

---

## 📊 Database Compatibility

### No Database Schema Changes

✅ All database tables remain unchanged
✅ Existing data preserved
✅ Backward compatible with old data

### Password Migration

**Old Passwords (Plain Text):**
- Still work but not recommended
- New registrations automatically hashed
- Consider rehashing old passwords on next update

**Recommendation:**
```python
# Optional: Rehash old passwords on next user login
from app.security import hash_password, verify_password

user = get_user_by_id(user_id)
if not is_bcrypt_hash(user['password']):
    # Old plain text password, rehash it
    hashed = hash_password(user['password'])
    update_user_password(user_id, hashed)
```

---

## 🚀 Deployment

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Verify bcrypt is installed
python -c "import bcrypt; print(bcrypt.__version__)"
```

### Deployment Steps

1. Pull the refactoring branch
2. Update requirements: `pip install -r requirements.txt`
3. Run app: `python run.py`
4. Test endpoints with cURL (see Testing section)
5. Update frontend/mobile app with new endpoints
6. Deploy!

---

## ⚠️ Breaking Changes

### For Frontend/Mobile Developers

**CRITICAL: Endpoint URLs have changed!**

| Old Endpoint | New Endpoint | Status |
|---|---|---|
| `/api/movies/{id}/reviews` | `/api/reviews/movies/{id}` | ⚠️ CHANGED |
| `/api/movies/{id}/favorites` | `/api/favorites/movies/{id}` | ⚠️ CHANGED |
| `/api/movies/{id}/ratings` | REMOVED | ❌ REMOVED |

### For Database

- ✅ No schema changes
- ✅ All data preserved
- ✅ Password hashing is transparent

---

## 📝 File Changes Summary

### New Files
- `app/security.py` - Password hashing utilities
- `app/reviews/schemas.py` - Review data schemas
- `app/reviews/router.py` - Review endpoints
- `app/favorites/schemas.py` - Favorite data schemas
- `app/favorites/router.py` - Favorite endpoints

### Modified Files
- `app/db.py` - Added password hashing
- `app/users/router.py` - Secure password verification
- `app/movies/router.py` - Removed reviews, favorites, ratings
- `app/main.py` - Added new routers
- `requirements.txt` - Added bcrypt

### Removed Files
- None (all functionality preserved)

---

## 🆘 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'bcrypt'

**Solution:**
```bash
pip install bcrypt>=4.0.0
```

### Issue: 404 on old endpoints

**Solution:**
Update your API calls to use new endpoints:
- `/api/movies/{id}/reviews` → `/api/reviews/movies/{id}`
- `/api/movies/{id}/favorites` → `/api/favorites/movies/{id}`

### Issue: Login fails after update

**Reason:** Old plain-text passwords need to be verified with new bcrypt system.

**Solution:**
Try with correct password. If it still fails, check:
1. Username exists
2. Password is correct
3. User registration after update uses new hashing

---

## 📚 Further Reading

- [Bcrypt Documentation](https://github.com/pyca/bcrypt)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/)

---

## ✅ Checklist for Migration

- [ ] Pull latest code from `refactor/modularize-and-hash-passwords`
- [ ] Install new dependencies: `pip install -r requirements.txt`
- [ ] Test password hashing with registration and login
- [ ] Update frontend API endpoints
- [ ] Test review endpoints with new URLs
- [ ] Test favorites endpoints with new URLs
- [ ] Remove ratings endpoint calls from frontend
- [ ] Deploy to production
- [ ] Monitor logs for any issues

---

**Questions?** Check the API documentation or create an issue!

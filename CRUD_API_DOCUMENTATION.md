# CRUD API Documentation

## Overview

This document describes the implemented CRUD (Create, Read, Update, Delete) operations for Users and Movies modules in the FastAPI project.

---

## Users Module CRUD Operations

### 1. CREATE - Register User
**Endpoint:** `POST /api/users/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "username": "john_doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "password": "password123",
  "is_user": true,
  "is_moderator": false,
  "is_admin": false
}
```

**Error Responses:**
- `400 Bad Request`: Email already exists

---

### 2. READ - Get User
**Endpoint:** `GET /api/users/me?user_id=1`

**Query Parameters:**
- `user_id` (required): User ID

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "password": "password123",
  "is_user": true,
  "is_moderator": false,
  "is_admin": false
}
```

**Error Responses:**
- `404 Not Found`: User not found

---

### 3. READ - Login User
**Endpoint:** `POST /api/users/login`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "password": "password123",
  "is_user": true,
  "is_moderator": false,
  "is_admin": false
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

### 4. UPDATE - Update User Profile
**Endpoint:** `PUT /api/users/{user_id}`

**Path Parameters:**
- `user_id` (required): User ID to update

**Request Body (all fields optional):**
```json
{
  "email": "newemail@example.com",
  "username": "new_username",
  "password": "newpassword123"
}
```

**Examples:**

**Update email only:**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

**Update username only:**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username": "new_username"}'
```

**Update password only:**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"password": "newpassword123"}'
```

**Update multiple fields:**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "username": "new_username",
    "password": "newpassword123"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "new_username",
  "password": "newpassword123",
  "is_user": true,
  "is_moderator": false,
  "is_admin": false
}
```

**Error Responses:**
- `404 Not Found`: User not found
- `400 Bad Request`: Email already exists / Username already exists

---

### 5. DELETE - Delete User
**Endpoint:** `DELETE /api/users/{user_id}`

**Path Parameters:**
- `user_id` (required): User ID to delete

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

**Response (200 OK):**
```json
{
  "status": "deleted",
  "user_id": 1
}
```

**Cascade Deletes:**
When a user is deleted, all related data is automatically removed:
- User's reviews
- User's ratings
- User's favorite movies

**Error Responses:**
- `404 Not Found`: User not found
- `500 Internal Server Error`: Failed to delete user

---

## Movies Module CRUD Operations

### 1. CREATE - Create Movie
**Endpoint:** `POST /api/movies/`

**Request Body:**
```json
{
  "title": "The Matrix",
  "description": "A computer programmer discovers...",
  "genre": "Sci-Fi",
  "year": 1999,
  "poster_url": "https://example.com/matrix.jpg"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "The Matrix",
  "description": "A computer programmer discovers...",
  "genre": "Sci-Fi",
  "year": 1999,
  "poster_url": "https://example.com/matrix.jpg"
}
```

---

### 2. READ - Get All Movies
**Endpoint:** `GET /api/movies/?genre=Sci-Fi&sort=title`

**Query Parameters:**
- `genre` (optional): Filter by genre
- `sort` (optional): Sort by 'title', 'year', or 'popular' (default)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "The Matrix",
    "description": "A computer programmer discovers...",
    "genre": "Sci-Fi",
    "year": 1999,
    "poster_url": "https://example.com/matrix.jpg"
  },
  {
    "id": 2,
    "title": "Inception",
    "description": "A skilled thief who steals corporate secrets...",
    "genre": "Sci-Fi",
    "year": 2010,
    "poster_url": "https://example.com/inception.jpg"
  }
]
```

---

### 3. READ - Get Single Movie
**Endpoint:** `GET /api/movies/{movie_id}`

**Path Parameters:**
- `movie_id` (required): Movie ID

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "The Matrix",
  "description": "A computer programmer discovers...",
  "genre": "Sci-Fi",
  "year": 1999,
  "poster_url": "https://example.com/matrix.jpg"
}
```

**Error Responses:**
- `404 Not Found`: Movie not found

---

### 4. DELETE - Delete Movie
**Endpoint:** `DELETE /api/movies/{movie_id}`

**Path Parameters:**
- `movie_id` (required): Movie ID to delete

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/movies/1
```

**Response (200 OK):**
```json
{
  "status": "deleted",
  "movie_id": 1
}
```

**Cascade Deletes:**
When a movie is deleted, all related data is automatically removed:
- Movie's reviews
- Movie's ratings
- Movie's favorites (from all users)

**Error Responses:**
- `404 Not Found`: Movie not found
- `500 Internal Server Error`: Failed to delete movie

---

## Database Functions

### Users Database Functions

```python
# Read operations
get_user_by_id(user_id: int) -> Optional[Dict]
get_user_by_email(email: str) -> Optional[Dict]
get_user_by_username(username: str) -> Optional[Dict]

# Create operation
create_user(email: str, password: str, username: str, is_moderator: bool = False) -> Dict

# Update operation
update_user(
    user_id: int,
    email: Optional[str] = None,
    password: Optional[str] = None,
    username: Optional[str] = None,
    is_moderator: Optional[bool] = None,
    is_admin: Optional[bool] = None
) -> Optional[Dict]

# Delete operation
delete_user(user_id: int) -> bool
```

### Movies Database Functions

```python
# Read operations
get_all_movies() -> List[Dict]
get_movie_by_id(movie_id: int) -> Optional[Dict]

# Create operation
create_movie(
    title: str,
    description: str,
    genre: str,
    year: int,
    poster_url: str = None
) -> Dict

# Delete operation
delete_movie(movie_id: int) -> bool
```

---

## Error Handling

All endpoints follow standard HTTP status codes:

| Status Code | Meaning | Example |
|-------------|---------|----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Duplicate email/username |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Database error |

---

## Data Validation

### Email Validation
- Must be valid email format
- Must be unique across all users

### Username Validation
- Must be unique across all users

### Movie Year
- Must be valid integer

### Password
- No minimum length requirement (can be improved in future)
- Stored as plain text (consider implementing hashing in future)

---

## Best Practices for API Usage

### 1. Always check response status codes
```python
import requests

response = requests.delete('http://localhost:8000/api/users/1')
if response.status_code == 200:
    print("User deleted successfully")
elif response.status_code == 404:
    print("User not found")
```

### 2. Use partial updates
```json
// Only update what you need
PUT /api/users/1
{"email": "newemail@example.com"}

// Instead of sending all fields
{
  "email": "newemail@example.com",
  "username": "existing_username",
  "password": "existing_password"
}
```

### 3. Handle cascade deletes carefully
```python
# When deleting a movie, all reviews/ratings are deleted
response = requests.delete('http://localhost:8000/api/movies/1')
# Make sure you really want to delete it
```

---

## Future Improvements

- [ ] Password hashing with bcrypt
- [ ] Authentication tokens (JWT)
- [ ] Authorization (admin-only deletion)
- [ ] Soft deletes (mark as deleted, don't remove)
- [ ] Audit logs (track who deleted what)
- [ ] Pagination for list endpoints
- [ ] Search/filter functionality
- [ ] Rate limiting
- [ ] API versioning

---

## Testing

See `QUICK_START.md` for testing instructions.

Example curl commands are provided in each endpoint description above.

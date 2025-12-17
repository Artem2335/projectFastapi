"""Populate database with sample data for testing"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import get_db_url
from app.database import Base
from app.users.models import User
from app.movies.models import Movie
from app.reviews.models import Review, Rating
from app.favorites.models import Favorite
import bcrypt

DATABASE_URL = get_db_url()

# Create async session factory
async_session = sessionmaker(
    create_async_engine(DATABASE_URL, echo=False),
    class_=AsyncSession,
    expire_on_commit=False
)

async def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def seed_db():
    """
    Populate database with sample data.
    Creates:
    - 3 users (regular, moderator, admin)
    - 5 movies
    - Sample reviews and ratings
    - Sample favorites
    """
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with AsyncSession(engine) as session:
        try:
            # Create sample users
            user1 = User(
                email="user1@example.com",
                password=await hash_password("password123"),
                username="john_doe",
                is_user=True,
                is_moderator=False,
                is_admin=False,
            )
            
            user2 = User(
                email="moderator@example.com",
                password=await hash_password("modpass123"),
                username="moderator",
                is_user=True,
                is_moderator=True,
                is_admin=False,
            )
            
            user3 = User(
                email="admin@example.com",
                password=await hash_password("adminpass123"),
                username="admin",
                is_user=True,
                is_moderator=True,
                is_admin=True,
            )
            
            session.add_all([user1, user2, user3])
            await session.flush()  # Get IDs without commit
            
            # Create sample movies
            movies_data = [
                {
                    "title": "The Matrix",
                    "description": "A hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                    "genre": "Sci-Fi",
                    "year": 1999,
                    "poster_url": "https://via.placeholder.com/300x450?text=The+Matrix",
                },
                {
                    "title": "Inception",
                    "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                    "genre": "Sci-Fi",
                    "year": 2010,
                    "poster_url": "https://via.placeholder.com/300x450?text=Inception",
                },
                {
                    "title": "The Dark Knight",
                    "description": "When the menace known as The Joker wreaks havoc, Batman must accept one of the greatest psychological and physical tests.",
                    "genre": "Action",
                    "year": 2008,
                    "poster_url": "https://via.placeholder.com/300x450?text=The+Dark+Knight",
                },
                {
                    "title": "Forrest Gump",
                    "description": "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man with an IQ of 75.",
                    "genre": "Drama",
                    "year": 1994,
                    "poster_url": "https://via.placeholder.com/300x450?text=Forrest+Gump",
                },
                {
                    "title": "Pulp Fiction",
                    "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
                    "genre": "Crime",
                    "year": 1994,
                    "poster_url": "https://via.placeholder.com/300x450?text=Pulp+Fiction",
                },
            ]
            
            movies = [Movie(**data) for data in movies_data]
            session.add_all(movies)
            await session.flush()  # Get IDs without commit
            
            # Create sample reviews
            reviews_data = [
                {
                    "movie_id": movies[0].id,
                    "user_id": user1.id,
                    "text": "Amazing sci-fi movie! The action sequences are incredible.",
                    "rating": 5,
                    "approved": True,
                },
                {
                    "movie_id": movies[0].id,
                    "user_id": user2.id,
                    "text": "Groundbreaking for its time. Still holds up today!",
                    "rating": 5,
                    "approved": True,
                },
                {
                    "movie_id": movies[1].id,
                    "user_id": user1.id,
                    "text": "Complex and mind-bending. Need to watch twice to understand everything.",
                    "rating": 4,
                    "approved": True,
                },
                {
                    "movie_id": movies[2].id,
                    "user_id": user2.id,
                    "text": "Best Batman movie ever made!",
                    "rating": 5,
                    "approved": True,
                },
                {
                    "movie_id": movies[3].id,
                    "user_id": user1.id,
                    "text": "Heartwarming and inspiring story.",
                    "rating": 4,
                    "approved": True,
                },
            ]
            
            reviews = [Review(**data) for data in reviews_data]
            session.add_all(reviews)
            await session.flush()
            
            # Create sample ratings
            ratings_data = [
                {"movie_id": movies[0].id, "user_id": user1.id, "value": 5.0},
                {"movie_id": movies[0].id, "user_id": user2.id, "value": 4.8},
                {"movie_id": movies[1].id, "user_id": user1.id, "value": 4.5},
                {"movie_id": movies[2].id, "user_id": user2.id, "value": 5.0},
                {"movie_id": movies[3].id, "user_id": user1.id, "value": 4.7},
                {"movie_id": movies[4].id, "user_id": user2.id, "value": 4.6},
            ]
            
            ratings = [Rating(**data) for data in ratings_data]
            session.add_all(ratings)
            await session.flush()
            
            # Create sample favorites
            favorites_data = [
                {"movie_id": movies[0].id, "user_id": user1.id},
                {"movie_id": movies[1].id, "user_id": user1.id},
                {"movie_id": movies[2].id, "user_id": user2.id},
                {"movie_id": movies[0].id, "user_id": user2.id},
            ]
            
            favorites = [Favorite(**data) for data in favorites_data]
            session.add_all(favorites)
            
            # Commit all changes
            await session.commit()
            
            print("\n" + "="*50)
            print("✅ DATABASE SEEDING SUCCESS!")
            print("="*50)
            print(f"👥 Users created:")
            print(f"   - john_doe (regular user)")
            print(f"   - moderator (moderator)")
            print(f"   - admin (admin)")
            print(f"🎬 Movies created: {len(movies)}")
            print(f"📝 Reviews created: {len(reviews)}")
            print(f"⭐ Ratings created: {len(ratings)}")
            print(f"❤️  Favorites created: {len(favorites)}")
            print("="*50)
            print("\n📝 Test Credentials:")
            print("   Regular User:  john_doe / password123")
            print("   Moderator:     moderator / modpass123")
            print("   Admin:         admin / adminpass123")
            print("="*50 + "\n")
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ ERROR seeding database: {e}\n")
            raise
        finally:
            await engine.dispose()

def main():
    """Run database seeding"""
    asyncio.run(seed_db())

if __name__ == "__main__":
    main()

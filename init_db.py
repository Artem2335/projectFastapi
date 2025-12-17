"""Initialize SQLite database using SQLAlchemy async"""
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from app.database import Base
from app.users.models import User
from app.movies.models import Movie
from app.reviews.models import Review, Rating
from app.favorites.models import Favorite
from app.config import get_db_url

DATABASE_URL = get_db_url()
DB_PATH = Path(__file__).parent / "kinovzor.db"

async def init_db():
    """
    Initialize database using SQLAlchemy.
    Creates all tables from models.
    """
    # Remove old database if exists
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"🗑️ Removed old database: {DB_PATH}")
    
    # Create async engine
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("\n" + "="*50)
        print("✅ DATABASE INITIALIZATION SUCCESS!")
        print("="*50)
        print(f"📁 Database: {DB_PATH}")
        print(f"📊 Tables created:")
        print(f"   - users")
        print(f"   - movies")
        print(f"   - reviews")
        print(f"   - ratings")
        print(f"   - favorites")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR initializing database: {e}\n")
        raise
    finally:
        await engine.dispose()

def main():
    """Run initialization"""
    asyncio.run(init_db())

if __name__ == "__main__":
    main()

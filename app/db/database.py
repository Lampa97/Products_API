"""
Database connection setup.

This module contains configuration for async PostgreSQL connection
using SQLAlchemy 2.0 and asyncpg driver.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create async database engine
# Replace postgresql:// with postgresql+asyncpg:// for async work
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,  # SQL query logging (disable in production)
    future=True,  # Use SQLAlchemy 2.0 syntax
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.
    
    This is a generator function that creates an async session,
    yields it, and then properly closes it after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # Rollback transaction on error
            await session.rollback()
            raise
        finally:
            # Always close the session
            await session.close()
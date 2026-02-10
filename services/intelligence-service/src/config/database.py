"""
Database configuration and connection
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from loguru import logger

from src.config.settings import settings

# Convert postgres:// to postgresql+asyncpg://
if settings.DATABASE_URL.startswith("postgresql://"):
    database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    database_url = settings.DATABASE_URL

# Create async engine
engine = create_async_engine(
    database_url,
    echo=settings.LOG_LEVEL == "DEBUG",
    poolclass=NullPool,  # Use NullPool for async
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database (create tables)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")

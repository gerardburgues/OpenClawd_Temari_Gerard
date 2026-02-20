import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import DATABASE_URL

_is_serverless = os.getenv("SKIP_CREATE_TABLES")

if _is_serverless:
    # Serverless + Supabase PgBouncer: use psycopg driver (no prepared stmt issues)
    _url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://")
    engine = create_async_engine(
        _url,
        echo=False,
        poolclass=NullPool,
        connect_args={"prepare_threshold": 0},
    )
else:
    # Local dev: asyncpg direct to PostgreSQL
    engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session

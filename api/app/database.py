import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import DATABASE_URL

# For PgBouncer transaction mode: disable prepared statement caching
_is_serverless = os.getenv("SKIP_CREATE_TABLES")
_sep = "&" if "?" in DATABASE_URL else "?"
_url = DATABASE_URL + _sep + "prepared_statement_cache_size=0&statement_cache_size=0" if _is_serverless else DATABASE_URL

engine = create_async_engine(
    _url,
    echo=False,
    poolclass=NullPool if _is_serverless else None,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session

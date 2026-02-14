import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://typed:typed_dev@localhost:5432/temarios",
)

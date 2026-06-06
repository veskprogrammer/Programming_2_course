"""Модуль настройки подключения к базе данных.

Содержит асинхронный движок SQLAlchemy, фабрику сессий,
базовый класс моделей и dependency-функцию для FastAPI.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL: str = "sqlite+aiosqlite:///./currency_api.db"

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей приложения."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Создать и вернуть асинхронную сессию базы данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        yield session

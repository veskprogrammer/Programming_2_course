"""Главный модуль FastAPI-приложения.

Файл создаёт объект приложения, подключает роутеры и создаёт таблицы
в базе данных при запуске сервера.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import currencies, subscriptions, users

app = FastAPI(
    title="Currency Tracker API",
    description="Лабораторная работа 3: REST API для отслеживания курсов валют",
    version="1.0.0",
)


@app.on_event("startup")
async def on_startup() -> None:
    """Создать таблицы базы данных при запуске приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root() -> dict[str, str]:
    """Вернуть сообщение о работоспособности API.

    Returns:
        dict[str, str]: Сообщение о состоянии приложения.
    """
    return {"message": "Currency Tracker API работает"}


app.include_router(users.router)
app.include_router(currencies.router)
app.include_router(subscriptions.router)

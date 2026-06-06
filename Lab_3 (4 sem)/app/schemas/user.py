"""Pydantic-схемы для работы с пользователями."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CurrencyShort(BaseModel):
    """Краткая схема валюты для отображения подписок пользователя."""

    code: str
    name: str
    rate: float | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Схема данных для создания пользователя."""

    username: str
    email: EmailStr


class UserUpdate(BaseModel):
    """Схема данных для обновления пользователя."""

    username: str | None = None
    email: EmailStr | None = None


class UserRead(BaseModel):
    """Схема данных для вывода информации о пользователе."""

    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithSubscriptions(UserRead):
    """Схема пользователя со списком валютных подписок."""

    currencies: list[CurrencyShort] = []

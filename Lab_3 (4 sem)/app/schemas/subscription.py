"""Pydantic-схемы для работы с подписками."""

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    """Схема данных для создания или удаления подписки."""

    user_id: int
    currency_code: str


class SubscriptionRead(BaseModel):
    """Схема ответа после операции с подпиской."""

    user_id: int
    currency_code: str
    message: str

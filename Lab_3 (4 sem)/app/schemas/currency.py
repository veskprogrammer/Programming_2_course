"""Pydantic-схемы для работы с валютами."""

from pydantic import BaseModel, ConfigDict


class CurrencyRead(BaseModel):
    """Схема данных для вывода валюты."""

    id: int
    code: str
    name: str
    rate: float | None = None

    model_config = ConfigDict(from_attributes=True)


class CurrencyRate(BaseModel):
    """Схема данных для вывода курса конкретной валюты."""

    code: str
    name: str
    rate: float | None = None

"""ORM-модели приложения.

В модуле описаны сущности пользователя, валюты и подписки.
Связь между пользователями и валютами реализована как many-to-many
через таблицу Subscription.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """Модель пользователя системы."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Currency(Base):
    """Модель валюты и её последнего сохранённого курса."""

    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="currency",
        cascade="all, delete-orphan",
    )


class Subscription(Base):
    """Модель подписки пользователя на валюту."""

    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="subscriptions")
    currency: Mapped["Currency"] = relationship(back_populates="subscriptions")

    __table_args__ = (
        UniqueConstraint("user_id", "currency_id", name="unique_user_currency"),
    )

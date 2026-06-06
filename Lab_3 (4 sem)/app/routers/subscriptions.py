"""Роутер для создания и удаления подписок на валюты."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Currency, Subscription, User
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionRead:
    """Создать подписку пользователя на валюту.

    Args:
        data: Данные подписки.
        db: Асинхронная сессия базы данных.

    Returns:
        SubscriptionRead: Результат создания подписки.
    """
    user = await db.get(User, data.user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    currency_code = data.currency_code.upper()
    result = await db.execute(select(Currency).where(Currency.code == currency_code))
    currency = result.scalar_one_or_none()

    if currency is None:
        raise HTTPException(
            status_code=404,
            detail="Валюта не найдена. Сначала выполните POST /currencies/update",
        )

    existing = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.currency_id == currency.id,
        )
    )

    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже подписан на эту валюту",
        )

    subscription = Subscription(user_id=user.id, currency_id=currency.id)
    db.add(subscription)
    await db.commit()

    return SubscriptionRead(user_id=user.id, currency_code=currency.code, message="Подписка создана")


@router.delete("/", response_model=SubscriptionRead)
async def delete_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
) -> SubscriptionRead:
    """Удалить подписку пользователя на валюту.

    Args:
        data: Данные подписки.
        db: Асинхронная сессия базы данных.

    Returns:
        SubscriptionRead: Результат удаления подписки.
    """
    user = await db.get(User, data.user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    currency_code = data.currency_code.upper()
    result = await db.execute(select(Currency).where(Currency.code == currency_code))
    currency = result.scalar_one_or_none()

    if currency is None:
        raise HTTPException(status_code=404, detail="Валюта не найдена")

    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.currency_id == currency.id,
        )
    )
    subscription = result.scalar_one_or_none()

    if subscription is None:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    await db.delete(subscription)
    await db.commit()

    return SubscriptionRead(user_id=user.id, currency_code=currency.code, message="Подписка удалена")

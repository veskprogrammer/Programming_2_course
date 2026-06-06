"""Роутер для CRUD-операций с пользователями."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.models import Subscription, User
from app.schemas.user import CurrencyShort, UserCreate, UserRead, UserUpdate, UserWithSubscriptions

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """Создать нового пользователя.

    Args:
        user_data: Данные для создания пользователя.
        db: Асинхронная сессия базы данных.

    Returns:
        User: Созданный пользователь.
    """
    user = User(username=user_data.username, email=user_data.email)
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким username или email уже существует",
        ) from error


@router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[User]:
    """Получить список всех пользователей.

    Args:
        db: Асинхронная сессия базы данных.

    Returns:
        list[User]: Список пользователей.
    """
    result = await db.execute(select(User))
    return list(result.scalars().all())


@router.get("/{user_id}", response_model=UserWithSubscriptions)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserWithSubscriptions:
    """Получить пользователя вместе со списком его подписок.

    Args:
        user_id: Идентификатор пользователя.
        db: Асинхронная сессия базы данных.

    Returns:
        UserWithSubscriptions: Пользователь со списком валют.
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.subscriptions).selectinload(Subscription.currency))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    currencies = [
        CurrencyShort(code=sub.currency.code, name=sub.currency.name, rate=sub.currency.rate)
        for sub in user.subscriptions
    ]

    return UserWithSubscriptions(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        currencies=currencies,
    )


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Обновить данные пользователя.

    Args:
        user_id: Идентификатор пользователя.
        user_data: Новые данные пользователя.
        db: Асинхронная сессия базы данных.

    Returns:
        User: Обновлённый пользователь.
    """
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user_data.username is not None:
        user.username = user_data.username

    if user_data.email is not None:
        user.email = user_data.email

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username или email уже используется",
        ) from error


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Удалить пользователя по идентификатору.

    Args:
        user_id: Идентификатор пользователя.
        db: Асинхронная сессия базы данных.

    Returns:
        dict[str, str]: Сообщение об успешном удалении.
    """
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    await db.delete(user)
    await db.commit()

    return {"message": "Пользователь удалён"}

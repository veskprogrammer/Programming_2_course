"""Роутер для работы с валютами и курсами."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Currency
from app.schemas.currency import CurrencyRate, CurrencyRead
from app.services.cbr import fetch_currencies_from_cbr

router = APIRouter(prefix="/currencies", tags=["Currencies"])


@router.get("/", response_model=list[CurrencyRead])
async def get_currencies(db: AsyncSession = Depends(get_db)) -> list[Currency]:
    """Получить список всех валют из локальной базы данных.

    Args:
        db: Асинхронная сессия базы данных.

    Returns:
        list[Currency]: Список валют.
    """
    result = await db.execute(select(Currency).order_by(Currency.code))
    return list(result.scalars().all())


@router.post("/update")
async def update_currencies(db: AsyncSession = Depends(get_db)) -> dict[str, int | str]:
    """Обновить список валют и курсов с сайта ЦБ РФ.

    Args:
        db: Асинхронная сессия базы данных.

    Returns:
        dict[str, int | str]: Информация о количестве добавленных и обновлённых валют.
    """
    currencies_data = await fetch_currencies_from_cbr()
    added = 0
    updated = 0

    for item in currencies_data:
        result = await db.execute(select(Currency).where(Currency.code == item["code"]))
        currency = result.scalar_one_or_none()

        if currency is None:
            currency = Currency(
                code=str(item["code"]),
                name=str(item["name"]),
                rate=float(item["rate"]),
            )
            db.add(currency)
            added += 1
        else:
            currency.name = str(item["name"])
            currency.rate = float(item["rate"])
            updated += 1

    await db.commit()

    return {"message": "Список валют и курсов обновлён", "added": added, "updated": updated}


@router.get("/{currency_code}/rate", response_model=CurrencyRate)
async def get_currency_rate(currency_code: str, db: AsyncSession = Depends(get_db)) -> CurrencyRate:
    """Получить последний сохранённый курс валюты.

    Args:
        currency_code: Буквенный код валюты, например USD или EUR.
        db: Асинхронная сессия базы данных.

    Returns:
        CurrencyRate: Информация о курсе валюты.
    """
    code = currency_code.upper()
    result = await db.execute(select(Currency).where(Currency.code == code))
    currency = result.scalar_one_or_none()

    if currency is None:
        raise HTTPException(status_code=404, detail="Валюта не найдена")

    return CurrencyRate(code=currency.code, name=currency.name, rate=currency.rate)

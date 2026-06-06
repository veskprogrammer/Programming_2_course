"""Сервис получения курсов валют с сайта Центрального банка РФ."""

import xml.etree.ElementTree as ET

import httpx

CBR_URL: str = "https://www.cbr.ru/scripts/XML_daily.asp"


async def fetch_currencies_from_cbr() -> list[dict[str, str | float]]:
    """Получить список валют и курсов с сайта ЦБ РФ.

    Returns:
        list[dict[str, str | float]]: Список словарей с кодом, названием и курсом валюты.
    """
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(CBR_URL)
        response.raise_for_status()

    root = ET.fromstring(response.content)
    currencies: list[dict[str, str | float]] = []

    for item in root.findall("Valute"):
        code = item.findtext("CharCode")
        name = item.findtext("Name")
        value_text = item.findtext("Value")
        nominal_text = item.findtext("Nominal")

        if not code or not name or not value_text:
            continue

        value = float(value_text.replace(",", "."))
        nominal = int(nominal_text or 1)
        rate = round(value / nominal, 4)

        currencies.append({"code": code, "name": name, "rate": rate})

    return currencies

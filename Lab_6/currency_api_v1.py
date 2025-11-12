import requests
import sys
import json


def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):

    """
    Получает курсы валют из API ЦБ РФ (Итерация 1).

    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str): URL API ЦБ РФ

    Returns:
        dict: Словарь с кодами валют и их курсами или None в случае ошибки
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if 'Valute' not in data:
            print(f"Ошибка: в ответе API отсутствуют курсы валют", file=sys.stdout)
            return None

        valutes = data['Valute']
        result = {}

        for code in currency_codes:
            if code not in valutes:
                print(f"Ошибка: валюта {code} не найдена в ответе API", file=sys.stdout)
                return None

            result[code] = valutes[code]['Value']

        return result

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}", file=sys.stdout)
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}", file=sys.stdout)
        return None
    except KeyError as e:
        print(f"Ошибка структуры данных: отсутствует ключ {e}", file=sys.stdout)
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stdout)
        return None
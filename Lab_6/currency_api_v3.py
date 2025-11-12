import requests
import json
import logging
from functools import wraps


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('currency_errors.log', encoding='utf-8')
    ]
)

logger = logging.getLogger('currency_api')


def log_errors(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result:
                logger.info(f"Успешно получены курсы для валют: {list(result.keys())}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к API: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")
            return None
        except KeyError as e:
            logger.error(f"Ошибка структуры данных: отсутствует ключ {e}")
            return None
        except ValueError as e:
            logger.error(f"Ошибка данных: {e}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return None

    return wrapper


@log_errors
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):

    """
    Получает курсы валют из API ЦБ РФ (Итерация 3).

    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str): URL API ЦБ РФ

    Returns:
        dict: Словарь с кодами валют и их курсами или None в случае ошибки
    """

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if 'Valute' not in data:
        raise ValueError("В ответе API отсутствуют курсы валют")

    valutes = data['Valute']
    result = {}

    for code in currency_codes:
        if code not in valutes:
            raise ValueError(f"Валюта {code} не найдена в ответе API")

        result[code] = valutes[code]['Value']

    return result
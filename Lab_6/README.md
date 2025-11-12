# Отчёт ЛР-6
### ИВТ-1.1, Киселев Георгий

### Цель работы

Разработать программу на языке Python для получения курсов валют через API Центрального банка РФ, реализовать три итерации улучшения функции с добавлением логирования ошибок и модульного тестирования.

---

### Текст задачи

Написать функцию `get_currencies(currency_codes, url)`, которая обращается к API по url (по умолчанию - https://www.cbr-xml-daily.ru/daily_json.js) и возвращает словарь курсов валют для валют из списка `currency_codes`.

**Требования:**
- В возвращаемом словаре ключи - символьные коды валют, значения - их курсы
- В случае ошибки запроса функция должна вернуть `None`
- Использовать функцию `get` модуля `requests`

**Итерации разработки:**
1. Базовая реализация с логированием ошибок через `sys.stdout`
2. Вынос логирования в декоратор
3. Использование модуля `logging` для логирования

**Тестирование должно включать:**
- Проверку ключей и значений возвращаемого словаря
- Проверку обработки исключений
- Проверку записей логов в поток вывода

---

### Описание алгоритма

**Основная функция `get_currencies`:**
- Выполняет HTTP GET запрос к API ЦБ РФ
- Парсит JSON ответ
- Извлекает курсы для запрошенных валют
- Обрабатывает различные типы ошибок

**Обрабатываемые исключения:**
- Ошибки запроса к API (`requests.exceptions.RequestException`)
- Ошибки декодирования JSON (`json.JSONDecodeError`)
- Отсутствие курсов валют в ответе
- Отсутствие валюты из списка `currency_codes`
- Ошибки структуры данных (`KeyError`)
- Неожиданные ошибки

---

### Код программы

#### Итерация 1: Базовая реализация с логированием в stdout

```python
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
```

#### Итерация 2: Логирование вынесено в декоратор

```python
import requests
import sys
import json
from functools import wraps


def log_errors_to_stdout(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}", file=sys.stdout)
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}", file=sys.stdout)
            return None
        except KeyError as e:
            print(f"Ошибка структуры данных: отсутствует ключ {e}", file=sys.stdout)
            return None
        except ValueError as e:
            print(f"Ошибка данных: {e}", file=sys.stdout)
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}", file=sys.stdout)
            return None

    return wrapper


@log_errors_to_stdout
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):

    """
    Получает курсы валют из API ЦБ РФ (Итерация 2).

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
```

#### Итерация 3: Использование модуля logging

```python
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
```

---

### Модульные тесты

```python
import unittest
from unittest.mock import patch, MagicMock
import io
import logging
import requests
import json

from currency_api_v1 import get_currencies as get_currencies_v1
from currency_api_v2 import get_currencies as get_currencies_v2
from currency_api_v3 import get_currencies as get_currencies_v3


class TestCurrencyAPI(unittest.TestCase):

    def setUp(self):

        self.valid_response_data = {
            'Valute': {
                'USD': {'Value': 75.5},
                'EUR': {'Value': 85.2}
            }
        }

    # Тесты для Итерации 1
    def test_v1_success(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            result = get_currencies_v1(['USD', 'EUR'])

            self.assertEqual(result, {'USD': 75.5, 'EUR': 85.2})

    def test_v1_missing_currency(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = get_currencies_v1(['INVALID'])

            self.assertIsNone(result)
            self.assertIn("не найдена в ответе API", mock_stdout.getvalue())

    # Тесты для Итерации 2
    def test_v2_success(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            result = get_currencies_v2(['USD', 'EUR'])

            self.assertEqual(result, {'USD': 75.5, 'EUR': 85.2})

    def test_v2_network_error(self):

        with patch('requests.get') as mock_get:

            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = get_currencies_v2(['USD'])

            self.assertIsNone(result)
            self.assertIn("Ошибка запроса к API", mock_stdout.getvalue())

    def test_v2_http_error(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
            mock_get.return_value = mock_response

            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = get_currencies_v2(['USD'])

            self.assertIsNone(result)
            self.assertIn("Ошибка запроса к API", mock_stdout.getvalue())

    # Тесты для Итерации 3
    def test_v3_success(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            with self.assertLogs('currency_api', level='INFO') as log:
                result = get_currencies_v3(['USD', 'EUR'])

            self.assertEqual(result, {'USD': 75.5, 'EUR': 85.2})
            self.assertIn("Успешно получены курсы", log.output[0])

    def test_v3_json_error(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()

            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)
            mock_get.return_value = mock_response

            with self.assertLogs('currency_api', level='ERROR') as log:
                result = get_currencies_v3(['USD'])

            self.assertIsNone(result)
            self.assertIn("Ошибка декодирования JSON", log.output[0])

    def test_v3_value_error(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            with self.assertLogs('currency_api', level='ERROR') as log:
                result = get_currencies_v3(['INVALID'])

            self.assertIsNone(result)
            self.assertIn("Ошибка данных", log.output[0])
            self.assertIn("не найдена в ответе API", log.output[0])

    # Общие тесты для всех версий
    def test_url_parameter(self):

        test_url = "https://custom-api.example.com"

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            get_currencies_v3(['USD'], url=test_url)

            mock_get.assert_called_once_with(test_url)

    def test_empty_list(self):

        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_response_data
            mock_get.return_value = mock_response

            result = get_currencies_v3([])

            self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

---

### Результаты выполнения

**Результаты тестирования:**
```
2025-11-12 16:08:38,706 - currency_api - Успешно получены курсы для валют: ['USD']


Ran 10 tests in 0.018s

OK
```

---

### Выводы

1. **Успешно реализованы** три итерации функции `get_currencies` с постепенным улучшением архитектуры и логирования
2. **Обеспечена надежная обработка ошибок** различных типов: сетевых, формата данных, структурных
3. **Применены принципы чистой архитектуры**: разделение ответственности через декораторы
4. **Реализовано комплексное тестирование** с использованием мок-объектов для изоляции тестов
5. **Достигнута полная покрываемость** основных сценариев работы функции
- Надежная обработка всех типов исключений
- Легкость тестирования и расширения функциональности

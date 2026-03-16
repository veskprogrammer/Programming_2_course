## Лабораторная работа №2
**Киселев Георгий**

**Группа: ИВТ 1.1**

### 1. Постановка задачи

Разработать программу для получения и преобразования данных о курсах валют, используя структурный паттерн проектирования «Декоратор».

**Требования к реализации:**
1.  **Базовый компонент:** Реализовать класс, который получает актуальные курсы валют с API Центрального банка РФ (ссылка на материалы ЛР 6 из 3 семестра). Базовый формат данных — список словарей.
2.  **Паттерн «Декоратор»:**
    *   Создать интерфейс (абстрактный класс) `DataProvider` с абстрактным методом `get_data`.
    *   Реализовать базовый класс `BaseDataDecorator`, хранящий ссылку на оборачиваемый объект и делегирующий ему вызовы.
    *   Реализовать конкретные декораторы для преобразования данных в форматы:
        *   **JSON** (используя встроенную библиотеку `json`).
        *   **CSV** (используя встроенную библиотеку `csv`).
        *   **YAML** (используя внешнюю библиотеку `PyYAML`, которую необходимо установить).
3.  **Функциональность декораторов:** Помимо метода `get_data`, возвращающего строку в соответствующем формате, каждый декоратор должен иметь метод `save_to_file(filename)`, который сохраняет эти данные в файл.
4.  **Оформление кода:**
    *   Аннотации типов (PEP-484).
    *   Документирование кода (Docstrings в стиле PEP-257).
    *   Соответствие стандартам оформления кода (PEP-8).
5.  **Тестирование:** Написать тесты с использованием `pytest` (минимум 2 теста для каждого декоратора и базового функционала).

### 2. Реализация

В ходе работы был спроектирован и реализован набор классов, демонстрирующих применение паттерна «Декоратор».

**Интерфейс `DataProvider` (Абстрактный класс):**
Определяет общий контракт для всех компонентов системы. Благодаря использованию `ABC` и `@abstractmethod`, гарантируется наличие метода `get_data` у всех "поставщиков данных".

**Конкретный компонент `CurrencyApiProvider`:**
Выступает в роли "ядра" системы. Его задача — сходить по указанному URL (API ЦБ РФ), скачать JSON с данными и преобразовать их в унифицированный список словарей (наш "базовый" формат). Он ничего не знает о CSV или YAML.

**Базовый декоратор `BaseDataDecorator`:**
Это "клей" паттерна. Он сам тоже реализует интерфейс `DataProvider`, но его основная цель — хранить ссылку на другой `DataProvider` (объект `_wrapped`) и передавать ему управление. Все остальные декораторы будут наследоваться от него.

**Конкретные декораторы (`JsonDecorator`, `CsvDecorator`, `YamlDecorator`):**
Их задача — "обернуть" базовый компонент или другой декоратор и добавить новое поведение. В данном случае они берут результат работы `_wrapped.get_data()` (список словарей) и преобразуют его в строку нужного формата. Декоратор `YamlDecorator` использует библиотеку `PyYAML` для сериализации, а `CsvDecorator` — встроенный модуль `csv`. Также каждый из них реализует метод `save_to_file` для записи результата на диск.

### 3. Исходный код

Основные части кода программы `currency_service.py`:

```python
import json
import csv
import io
import yaml  # pip install PyYAML
import requests
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DataProvider(ABC):
    """Интерфейс для всех поставщиков данных (как базовых, так и декорированных)."""

    @abstractmethod
    def get_data(self) -> Any:
        """Возвращает данные в некотором представлении."""
        pass


class CurrencyApiProvider(DataProvider):
    """Конкретный компонент. Запрашивает курсы валют с сервера ЦБ РФ."""

    def __init__(self, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> None:
        self.__url = url

    def get_data(self) -> List[Dict[str, Any]]:
        """Выполняет HTTP-запрос и парсит JSON от ЦБ в список словарей."""
        try:
            response = requests.get(self.__url, timeout=10)
            response.raise_for_status()
            data = response.json()
            valutes = data.get("Valute", {})
            return [
                {"code": k, "name": v["Name"], "value": v["Value"]}
                for k, v in valutes.items()
            ]
        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            return []


class BaseDataDecorator(DataProvider):
    """
    Базовый декоратор.
    Хранит ссылку на объект DataProvider и делегирует ему выполнение.
    """

    def __init__(self, wrapped: DataProvider) -> None:
        self._wrapped = wrapped

    def get_data(self) -> Any:
        return self._wrapped.get_data()


class JsonDecorator(BaseDataDecorator):
    """Декоратор, преобразующий данные в JSON-строку."""

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        return json.dumps(data, indent=4, ensure_ascii=False)

    def save_to_file(self, filename: str) -> None:
        """Сохраняет JSON-представление данных в файл."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.get_data())


class CsvDecorator(BaseDataDecorator):
    """Декоратор, преобразующий данные в CSV-строку."""

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue().strip()

    def save_to_file(self, filename: str) -> None:
        """Сохраняет CSV-представление данных в файл."""
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.get_data())


class YamlDecorator(BaseDataDecorator):
    """Декоратор, преобразующий данные в YAML-строку с помощью библиотеки PyYAML."""

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        # Используем pyyaml для генерации YAML
        return yaml.dump(data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, filename: str) -> None:
        """Сохраняет YAML-представление данных в файл."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.get_data())


if __name__ == "__main__":
    # Пример использования
    api_provider = CurrencyApiProvider()
    
    json_view = JsonDecorator(api_provider)
    print("--- JSON ---")
    print(json_view.get_data()[:500] + "...") # Покажем начало
    
    # json_view.save_to_file("rates.json")
    
    csv_view = CsvDecorator(api_provider)
    # csv_view.save_to_file("rates.csv")
```

### 4. Тестирование

Для проверки корректности работы программы использовалась библиотека `pytest`. Были созданы мок-объекты (`MockProvider`), чтобы тесты не зависели от наличия интернета или работоспособности внешнего API.

*   **Тест 1:** Проверяет, что `JsonDecorator` возвращает валидную JSON-строку, которую можно распарсить обратно.
*   **Тест 2:** Проверяет, что `CsvDecorator` правильно формирует заголовки и строки с данными.
*   **Тест 3:** Проверяет, что `YamlDecorator` создает строку, содержащую характерные для YAML элементы (дефисы, отступы).
*   **Тест 4:** Проверяет поведение всех декораторов при получении пустого списка данных от базового компонента.

```python
import pytest
import json
import yaml
from currency_service import DataProvider, JsonDecorator, CsvDecorator, YamlDecorator


class MockProvider(DataProvider):
    """Заглушка для имитации работы API с фиксированными данными."""
    def get_data(self):
        return [
            {"code": "USD", "name": "Доллар США", "value": 75.5},
            {"code": "EUR", "name": "Евро", "value": 82.1}
        ]

@pytest.fixture
def mock_provider():
    """Фикстура для инициализации мок-провайдера."""
    return MockProvider()


def test_json_decorator_format(mock_provider):
    """Проверяем, что на выходе валидный JSON."""
    decorator = JsonDecorator(mock_provider)
    result = decorator.get_data()
    
    parsed_data = json.loads(result)
    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2
    assert parsed_data[0]["code"] == "USD"


def test_csv_decorator_content(mock_provider):
    """Проверяем структуру CSV (заголовки и данные)."""
    decorator = CsvDecorator(mock_provider)
    result = decorator.get_data()
    
    lines = result.splitlines()
    assert lines[0] == "code,name,value"
    # Проверяем, что данные есть, порядок может отличаться
    assert any("USD,Доллар США,75.5" in line for line in lines[1:])


def test_yaml_decorator_structure(mock_provider):
    """Проверяем, что результат является валидным YAML и содержит нужные ключи."""
    decorator = YamlDecorator(mock_provider)
    result = decorator.get_data()
    
    # Проверяем, что это валидный YAML
    parsed_data = yaml.safe_load(result)
    assert isinstance(parsed_data, list)
    assert parsed_data[0]['code'] == "USD"
    
    # Проверяем характерные черты строки
    assert result.startswith("- code: USD")


def test_decorators_with_empty_data():
    """Проверяем, как декораторы ведут себя, если данных нет."""
    class EmptyProvider(DataProvider):
        def get_data(self): return []
        
    empty_provider = EmptyProvider()
    
    assert JsonDecorator(empty_provider).get_data() == "[]"
    assert CsvDecorator(empty_provider).get_data() == ""
    assert YamlDecorator(empty_provider).get_data() == "[]\n" # PyYAML так представляет пустой список


def test_save_to_file_methods(mock_provider, tmp_path):
    """Проверяем, что методы сохранения создают файлы."""
    json_dec = JsonDecorator(mock_provider)
    csv_dec = CsvDecorator(mock_provider)
    yaml_dec = YamlDecorator(mock_provider)
    
    temp_dir = tmp_path
    json_file = temp_dir / "test.json"
    csv_file = temp_dir / "test.csv"
    yaml_file = temp_dir / "test.yaml"
    
    json_dec.save_to_file(json_file)
    csv_dec.save_to_file(csv_file)
    yaml_dec.save_to_file(yaml_file)
    
    assert json_file.exists()
    assert csv_file.exists()
    assert yaml_file.exists()
    
    # Проверяем, что файлы не пустые
    assert json_file.stat().st_size > 0
    assert csv_file.stat().st_size > 0
    assert yaml_file.stat().st_size > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
```

### 5. Выводы

В ходе выполнения лабораторной работы был изучен и применен на практике структурный паттерн проектирования «Декоратор».

1.  **Гибкость расширения:** Паттерн позволил создать систему, в которой легко добавлять новые форматы вывода (например, XML), просто создавая новые классы-декораторы, не изменяя существующий код базового компонента (`CurrencyApiProvider`).
2.  **Принцип единственной ответственности:** Каждый класс отвечает за свою четко определенную задачу: базовый компонент — за получение "сырых" данных, декораторы — за их преобразование в конкретный формат.
3.  **Композиция вместо наследования:** Вместо того чтобы создавать множество подклассов типа `CurrencyApiJsonProvider`, `CurrencyApiCsvProvider` и т.д., мы динамически оборачиваем объекты, комбинируя их поведение.
4.  **Работа с внешними библиотеками:** Была успешно интегрирована библиотека `PyYAML` для сериализации данных, а также использованы встроенные модули `json` и `csv` и `requests` для работы с сетью.
5.  **Тестируемость:** Использование интерфейсов и внедрение зависимостей (через конструктор `BaseDataDecorator`) позволило легко подменять реальный поход в сеть на мок-объект, что сделало тесты быстрыми и надежными.

Таким образом, паттерн «Декоратор» является эффективным инструментом для расширения функциональности объектов во время выполнения программы, следуя принципам гибкой архитектуры ПО.

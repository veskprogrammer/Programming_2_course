import json
import csv
import io
import requests
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DataProvider(ABC):
    """
    Интерфейс для поставщиков данных.
    Гарантирует наличие метода get_data.
    """

    @abstractmethod
    def get_data(self) -> List[Dict[str, Any]]:
        """Возвращает список словарей с данными."""
        pass


class CurrencyApiProvider(DataProvider):
    """
    Запрашивает курсы валют с сервера ЦБ РФ.
    """

    def __init__(self, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> None:
        self.__url = url

    def get_data(self) -> List[Dict[str, Any]]:
        """Выполняет HTTP-запрос и парсит JSON ответ."""
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
    Базовый декоратор. Хранит ссылку на объект DataProvider 
    и делегирует ему выполнение основного метода.
    """

    def __init__(self, wrapped: DataProvider) -> None:
        self._wrapped = wrapped

    def get_data(self) -> Any:
        return self._wrapped.get_data()


class JsonDecorator(BaseDataDecorator):
    """Декоратор для вывода данных в формате JSON."""

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        return json.dumps(data, indent=4, ensure_ascii=False)


class CsvDecorator(BaseDataDecorator):
    """Декоратор для вывода данных в формате CSV."""

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        if not data:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue().strip()


class YamlDecorator(BaseDataDecorator):
    """
    Декоратор для вывода данных в формате YAML.
    Реализован вручную, чтобы избежать лишних зависимостей.
    """

    def get_data(self) -> str:
        data = self._wrapped.get_data()
        lines = []
        for item in data:
            lines.append("-")
            for key, value in item.items():
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)


if __name__ == "__main__":

    api_provider = CurrencyApiProvider()

    csv_view = CsvDecorator(api_provider)
    print("--- ПЕРВЫЕ 3 ВАЛЮТЫ В CSV ---")
    print("\n".join(csv_view.get_data().splitlines()[:4]))

    yaml_view = YamlDecorator(api_provider)
    print("\n--- YAML ФОРМАТ ---")
    print("\n".join(yaml_view.get_data().splitlines()[:6]))

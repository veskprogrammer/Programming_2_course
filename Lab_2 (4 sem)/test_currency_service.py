import pytest
import json
from currency_service import DataProvider, JsonDecorator, CsvDecorator, YamlDecorator


class MockProvider(DataProvider):
    """Заглушка для имитации работы API."""
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
    """Проверяем, что на выходе валидный JSON-текст."""
    decorator = JsonDecorator(mock_provider)
    result = decorator.get_data()
    
    parsed_data = json.loads(result)
    assert isinstance(parsed_data, list)
    assert parsed_data[0]["code"] == "USD"


def test_csv_decorator_content(mock_provider):
    """Проверяем структуру CSV (заголовки и данные)."""
    decorator = CsvDecorator(mock_provider)
    result = decorator.get_data()
    
    lines = result.splitlines()
    assert lines[0] == "code,name,value"
    assert "USD,Доллар США,75.5" in lines[1]


def test_yaml_decorator_structure(mock_provider):
    """Проверяем специфический YAML-синтаксис (дефисы)."""
    decorator = YamlDecorator(mock_provider)
    result = decorator.get_data()
    
    assert result.startswith("-")
    assert "  code: USD" in result
    assert "  value: 82.1" in result


def test_decorators_with_empty_data():
    """Проверяем, как декораторы ведут себя, если данных нет."""
    class EmptyProvider(DataProvider):
        def get_data(self): return []
        
    empty_provider = EmptyProvider()
    
    assert JsonDecorator(empty_provider).get_data() == "[]"
    assert CsvDecorator(empty_provider).get_data() == ""
    assert YamlDecorator(empty_provider).get_data() == ""

if __name__ == "__main__":
    pytest.main(["-v", __file__])
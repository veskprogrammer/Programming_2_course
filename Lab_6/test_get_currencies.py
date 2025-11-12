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
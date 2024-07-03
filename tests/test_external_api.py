import pytest
import requests
import json
from unittest.mock import patch
from src.external_api import convert_currency


@pytest.mark.parametrize(
    "transaction, expected_amount",
    [
        ({"amount": 100, "currency": "USD"}, 7000),
        ({"amount": 100, "currency": "EUR"}, 8750),
    ],
)
@patch("src.external_api.requests.get")
def test_convert_currency(mock_get, transaction, expected_amount):
    """Тест для конвертации в рубли"""
    mock_get.return_value.json.return_value = {"result": expected_amount}
    converted_amount = convert_currency(transaction)
    assert converted_amount == expected_amount

    print(f"Converted amount: {converted_amount} RUB")


def test_convert_currency_rub():
    """Тест для обработки рублей"""
    transaction = {"amount": 100, "currency": "RUB"}

    converted_amount = convert_currency(transaction)
    assert converted_amount == 100


def test_convert_currency_error(mock_requests_get):
    """Тест для обработки исключения RequestException в convert_currency"""
    transaction = {"amount": 100, "currency": "USD"}

    mock_requests_get.side_effect = requests.exceptions.RequestException("Connection error")
    converted_amount = convert_currency(transaction)
    assert converted_amount is None

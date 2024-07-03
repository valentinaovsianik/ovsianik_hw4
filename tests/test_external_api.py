import pytest
import requests
import json
from unittest.mock import patch
from src.external_api import convert_currency


real_file_path = "../data/operations.json"

with open(real_file_path, "r", encoding="utf-8") as file:
    transactions_data = json.load(file)


@pytest.mark.parametrize(
    "transaction, expected_amount",
    [
        ({"amount": 100, "currency": "USD"}, 7000),
        ({"amount": 100, "currency": "EUR"}, 8750),
    ],
)
def test_convert_currency(transaction, expected_amount, mock_requests_get):
    """Тест для конвертации рубли"""
    mock_requests_get.return_value.json.return_value = {"rates": {"RUB": 70, "USD": 1, "EUR": 0.8}}
    converted_amount = convert_currency(transaction)
    assert converted_amount == expected_amount


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

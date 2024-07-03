import pytest
import requests
from unittest.mock import patch
from src.external_api import convert_currency


def test_convert_currency_usd(mock_requests_get):
    """Тест для конвертации из долларов в рубли"""
    transaction = {"amount": 100, "currency": "USD"}

    mock_requests_get.return_value.json.return_value = {"rates": {"RUB": 70, "USD": 1, "EUR": 0.8}}
    converted_amount = convert_currency(transaction)
    assert converted_amount == 7000


def test_convert_currency_eur(mock_requests_get):
    """Тест для конвертации из евро в рубли"""
    transaction = {"amount": 100, "currency": "EUR"}

    mock_requests_get.return_value.json.return_value = {"rates": {"RUB": 70, "USD": 1, "EUR": 0.8}}
    converted_amount = convert_currency(transaction)
    assert converted_amount == 8750  # 100 * (70 / 0.8)


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

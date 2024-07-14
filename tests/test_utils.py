import json
import os
from unittest.mock import mock_open, patch

import pandas as pd
import re
import pytest

from src.utils import read_transactions, search_transactions, categorize_transactions


def test_file_exists_and_valid_data(mock_exists_true):
    """Тест: файл есть и содержит корректные данные"""
    transactions_data = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(transactions_data))) as mock_file:
        result = read_transactions("dummy_operations.json")
        assert result == transactions_data
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")


def test_file_does_not_exist(mock_exists_false):
    """Тест: файл не существует"""
    result = read_transactions("dummy_operations.json")
    assert result == []


def test_file_exists_and_empty_data(mock_exists_true):
    """Тест: файл есть, но пустой"""
    with patch("builtins.open", mock_open(read_data="[]")) as mock_file:
        result = read_transactions("dummy_operations.json")
        assert result == []
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")


def test_empty_file(mock_exists_true):
    """Тест для пустого файла"""
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        result = read_transactions("dummy_operations.json")
        assert result == []
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")


def test_error_file_reading(mock_exists_true):
    """Тест: ошибка при чтении файла"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = OSError
        result = read_transactions("dummy_operations.json")
        assert result == []
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")


def test_file_reading_with_other_error(mock_exists_true):
    """Тест: когда возникает ошибка IOError при чтении"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError
        result = read_transactions("dummy_operations.json")
        assert result == []
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")


def test_read_transactions_with_invalid_json(mock_exists_true):
    """Тест для случая, когда json неверный"""
    mock_open_data = "{'key': 'value'"  # Неверный json (нет закрывающей скобки
    with patch("builtins.open", mock_open(read_data=mock_open_data)):
        result = read_transactions("dummy_operations.json")
        assert result == []


def test_read_transactions_with_non_list(mock_exists_true):
    """Тест: когда содержимое файла не список"""
    mock_open_data = "{'key': 'value'}"  # Неверный формат данных (словарь, а не список)
    with patch("builtins.open", mock_open(read_data=mock_open_data)):
        result = read_transactions("dummy_operations.json")
        assert result == []


def test_read_transactions_with_invalid_encoding():
    """Тест: когда файл c неверной кодировкой"""
    mock_open_data = b"{}"
    with patch("builtins.open", mock_open(read_data=mock_open_data)) as mock_file:
        mock_file.side_effect = UnicodeDecodeError("utf-8", b"{}", 0, 1, "Mock decode error")
        result = read_transactions("dummy_operations.json")
    assert result == []


def test_read_transactions_nonexistent_file():
    """Тест: на несуществующий файл"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError
        result = read_transactions("dummy_operations.json")
        assert result == []


def test_read_transactions_with_string(mock_exists_true):
    """Тест: когда содержимое файла строка"""
    mock_open_data = '"string_data"'
    with patch("builtins.open", mock_open(read_data=mock_open_data)):
        result = read_transactions("dummy_operations.json")
        assert result == []


# Тест для проверки чтения csv-файла
@patch("src.utils.pd.read_csv")
@patch("os.path.exists", return_value=True)
def test_read_transactions_csv(mock_exists, mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
    result = read_transactions("dummy_operations.csv")
    assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    mock_read_csv.assert_called_once_with("dummy_operations.csv", sep=";")


# Тест для проверки чтения XLSX-файла
@patch("src.utils.pd.read_excel")
@patch("os.path.exists", return_value=True)
def test_read_transactions_xlsx(mock_exists, mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
    expected_result = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    result = read_transactions("dummy_operations.xlsx")
    assert result == expected_result
    mock_read_excel.assert_called_once_with("dummy_operations.xlsx")


# Тест для поиска в CSV-файле
def test_search_transactions_by_description_csv(csv_transactions_data):
    results = search_transactions(csv_transactions_data, "Перевод организации")
    assert any(transaction["description"] == "Перевод организации" for transaction in results)


# Тест для поиска в xlsx-файле
def test_search_transactions_by_description_xlsx(xlsx_transactions_data):
    results = search_transactions(xlsx_transactions_data, "Перевод организации")
    assert any(transaction["description"] == "Перевод организации" for transaction in results)


# Тест для поиска в json-файле
def test_search_transactions_by_description_json(json_transactions_data):
    results = search_transactions(json_transactions_data, "Перевод организации")
    assert any(transaction["description"] == "Перевод организации" for transaction in results)


# Тест для categorize_transactions
def test_categorize_transactions():
    transactions = [
        {"id": 650703, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z", "amount": 16210, "currency_name": "Sol",
         "currency_code": "PEN", "from": "Счет 58803664561298323391", "to": "Счет 39745660563456619397",
         "description": "Перевод организации"},
        {"id": 3598919, "state": "EXECUTED", "date": "2020-12-06T23:00:58Z", "amount": 29740, "currency_name": "Peso",
         "currency_code": "COP", "from": "Discover 3172601889670065", "to": "Discover 0720428384694643",
         "description": "Перевод с карты на карту"},
        {"id": 593027, "state": "CANCELED", "date": "2023-07-22T05:02:01Z", "amount": 30368,
         "currency_name": "Shilling", "currency_code": "TZS", "from": "Visa 1959232722494097",
         "to": "Visa 6804119550473710", "description": "Перевод с карты на карту"},
        {"id": 366176, "state": "EXECUTED", "date": "2020-08-02T09:35:18Z", "amount": 29482, "currency_name": "Rupiah",
         "currency_code": "IDR", "from": "Discover 0325955596714937", "to": "Visa 3820488829287420",
         "description": "Перевод с карты на карту"}
        ]

    categories = ["Перевод организации", "Перевод с карты на карту"]
    expected_result = {"Перевод организации": 1, "Перевод с карты на карту": 3}
    assert categorize_transactions(transactions, categories) == expected_result

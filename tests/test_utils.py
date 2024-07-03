import pytest
import json
from unittest.mock import mock_open, patch
from src.utils import read_transactions


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


def test_error_file_reading(mock_exists_true):
    """Тест: ошибка при чтении файла"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = OSError
        result = read_transactions("dummy_operations.json")
        assert result == []
        mock_file.assert_called_once_with("dummy_operations.json", "r", encoding="utf-8")

import pytest
import json
from unittest.mock import mock_open, patch
from src.utils import read_transactions

real_file_path = "../data/operations.json"

with open(real_file_path, "r", encoding="utf-8") as file:
    transactions_data = json.load(file)


def test_file_exists_and_valid_data(mock_exists_true):
    """Тест: файл есть и содержит корректные данные"""
    with patch("builtins.open", mock_open(read_data=json.dumps(transactions_data))) as mock_file:
        result = read_transactions(real_file_path)
        assert result == transactions_data
        mock_file.assert_called_once_with(real_file_path, "r", encoding="utf-8")


def test_file_does_not_exist(mock_exists_false):
    """Тест: файл не существует"""
    result = read_transactions(real_file_path)
    assert result == []


def test_file_exists_and_empty_data(mock_exists_true):
    """Тест: файл есть, но пустой"""
    with patch("builtins.open", mock_open(read_data="[]")) as mock_file:
        result = read_transactions(real_file_path)
        assert result == []
        mock_file.assert_called_once_with(real_file_path)


def test_error_file_reading(mock_exists_true):
    """Тест: ошибка при чтении файла"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = OSError
        result = read_transactions(real_file_path)
        assert result == []
        mock_file.assert_called_once_with(real_file_path)

import pytest
from unittest.mock import mock_open, patch
from src.utils import read_transactions


def test_file_exists_and_valid_data(mock_exists_true):
    """Тест: файл есть и содержит корректные данные"""
    with patch("builtins.open", mock_open(read_data="""[{"amount": 100}, {"amount": 200}]""")) as mock_file:
        result = read_transactions("dummy_path")
        assert result == [{"amount": 100}, {"amount": 200}]
        mock_exists_true.assert_called_once()
        mock_file.assert_called_once_with("dummy_path", "r", encoding="utf-8")

def test_file_does_not_exist(mock_exists_false):
    """Тест: файл не существует"""
    result = read_transactions("dummy_path")
    assert result == []
    mock_exists_false.assert_called_once()

def test_error_file_reading(mock_exists_true):
    """Тест: ошибка при чтении файла"""
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = OSError
        result = read_transactions("dummy_path")
        assert result == []
        mock_exists_true.assert_called_once()
        mock_file.assert_called_once_with("dummy_path", "r", encoding="utf-8")

import pytest

from src.masks import get_mask_card_number, get_mask_account

from src.widget import mask_account_card, get_data

@pytest.mark.parametrize("input_data, expected_output", [
    ("Visa Platinum 7000 7922 8960 6361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("Счет 35383033474447895560", "Счет **5560"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
])
def test_mask_account_card(input_data, expected_output):
    assert mask_account_card(input_data) == expected_output

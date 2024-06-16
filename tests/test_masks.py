import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("account_number, expected_output", [
                          ("73654108430135874305", "**4305"),
                          ("35383033474447895560", "**5560")
                         ])
def test_get_mask_account(account_number, expected_output):
    assert get_mask_account(account_number) == expected_output

def test_get_mask_account_error():
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("123abc456")


def test_get_mask_account_length():
    with pytest.raises(ValueError, match="Номер счета должен состоять не менее чем из 4 цифр"):
        get_mask_account("123")


@pytest.mark.parametrize("card_number, expected_output", [
                          ("7000792289606361", "7000 79** **** 6361"),
                          ("1596837868705199", "1596 83** **** 5199")])
def test_get_mask_card_number(card_number, expected_output):
    assert get_mask_card_number(card_number) == expected_output

def test_get_mask_card_number_length():
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр"):
        get_mask_card_number("123456")

    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("12345678ab111111")

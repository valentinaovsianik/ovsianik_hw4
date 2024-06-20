import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тест для  функции filter_by_currency
def test_filter_by_currency(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    operation_ids = [next(usd_transactions)["id"] for _ in range(2)]
    expected_ids = [939719570, 142264268]
    assert operation_ids == expected_ids


# Тест для transaction_descriptions
@pytest.mark.parametrize(
    "expected_descriptions",
    [
        [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ],
    ],
)
def test_transaction_descriptions(transactions, expected_descriptions):
    descriptions = transaction_descriptions(transactions)
    for expected_description in expected_descriptions:
        actual_description = next(descriptions)
        assert actual_description == expected_description


def test_transaction_description_print(transactions):
    descriptions = transaction_descriptions(transactions)

    for _ in range(5):
        print(next(descriptions))


# Тест для card_number_generator
def test_card_number_generator():
    expected_card_numbers = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    card_numbers_generator = card_number_generator(1, 5)

    for expected_card_number in expected_card_numbers:
        actual_card_number = next(card_numbers_generator)
        assert actual_card_number == expected_card_number

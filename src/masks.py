
def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты в формате XXXX XX** **** XXXX"""
    if len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета в формате **XXXX"""
    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(account_number) < 4:
        raise ValueError("Номер счета должен состоять не менее чем из 4 цифр")
    return f"**{account_number[-4:]}"


# Пример работы функции, которая возвращает маску карты
# card_number = "7000792289606361"
# print(get_mask_card_number(card_number))
#
# # Пример работы функции, которая возвращает маску карты
# account_number = "73654108430135874305"
# print(get_mask_account(account_number))

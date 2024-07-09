import logging
import os.path
from datetime import datetime

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, "masks.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты в формате XXXX XX** **** XXXX"""
    logger.info(f"Запущена функция get_mask_card_number с параметром {card_number}")
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16:
        error_message = "Номер карты должен состоять из 16 цифр"
        logger.error(error_message)
        raise ValueError(error_message)
    if not card_number.isdigit():
        error_message = "Номер карты должен содержать только цифры"
        logger.error(error_message)
        raise ValueError(error_message)
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Успешно замаскированный номер карты: {masked_number}")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета в формате **XXXX"""
    logger.info(f"Запущена функция get_mask_account с параметром {account_number}")
    if len(account_number) < 4:
        error_message = "Номер счета должен состоять не менее чем из 4 цифр"
        logger.error(error_message)
        raise ValueError(error_message)
    if not account_number.isdigit():
        error_message = "Номер счета должен содержать только цифры"
        logger.error(error_message)
        raise ValueError(error_message)
    masked_account = f"**{account_number[-4:]}"
    logger.info(f"Успешно замаскированный номер счета: {masked_account}")
    return masked_account


# Примеры работы функций
if __name__ == "__main__":
    card_number = "7000792289606361"
    account_number = "73654108430135874305"

    print(get_mask_card_number(card_number))
    print(get_mask_account(account_number))

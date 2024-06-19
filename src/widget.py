from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция принимает строку с типом карты/счета и номер и возвращает строку с замаскированным номером"""
    letters = ""
    digits = ""

    for char in info:  # Разделение букв и цифр из исходной строки
        if char.isdigit():
            digits += char
        elif char.isalpha() or char.isspace():
            letters += char

    letters = letters.rstrip()  # Убираем лишние пробелы в конце строки

    if info.lower().startswith("счет"):  # Определяем, маскировать номер счета или карты
        masked_number = get_mask_account(digits)
    else:
        masked_number = get_mask_card_number(digits)

    return f"{letters} {masked_number}"


# print(mask_account_card("Visa Platinum 7000 7922 8960 6361"))
# print(mask_account_card("Счет 73654108430135874305"))


def get_data(date_str: str) -> str:
    """Функция преобразует строку из формата 2018-07-11T02:26:18.671407 в формат 11.07.2018"""
    date_part = date_str.split("T")[0]  # Разделяем строку по символу "T"
    year, month, day = date_part.split("-")  # Разделяем дату через "-"
    return f"{day}.{month}.{year}"  # Возвращаем строку в нужном формате


# print(get_data("2018-07-11T02:26:18.671407"))

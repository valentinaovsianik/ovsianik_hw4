def mask_account_card(info: str) -> str:
    """Функция принимает строку с типом карты/счета и номер и возвращает строку с замаскированным номером"""

    def get_mask_card_number(card_num: str) -> str:
        """Функция маскирует номер карты в формате XXXX XX** **** XXXX"""
        card_num = card_num.replace(" ", "")
        if len(card_num) != 16 or not card_num.isdigit():
            raise ValueError("Номер карты  должен состоять из 16 цифр")
        return f"{card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"

    def get_mask_account(account_num: str) -> str:
        """Функция маскирует номер счета в формате **XXXX"""
        if len(account_num) < 4 or not account_num.isdigit():
            raise ValueError("Номер счета должен состоять не менее чем из 4 цифр")
        return f"**{account_num[-4:]}"

    parts = info.split(maxsplit=1)  # Разбиваем строку по 1 пробелу
    if len(parts) != 2:
        raise ValueError("Неверный формат данных")

    account_type, account_number = parts[0], parts[0]  # Берем элементы

    if account_type.lower() == "счет":
        masked_number = get_mask_account(account_number)  # Маскируем номер счета
        return f"{account_type} {masked_number}"  # Возвращаем строку с замаскированным номером счета
    else:
        try:
        masked_number = get_mask_card_number(account_number)  # Пытаемся маскировать номер карты
        except ValueError:
        masked_number = account_number # Если неполучилось, возвращаем как есть

    return f"{account_type} {masked_number}"  # Возвращаем строку с замаскированным номером карты


# print(mask_account_card("Visa Platinum 7000 7922 8960 6361"))
# print(mask_account_card("Счет 73654108430135874305"))


def get_data(date_str: str) -> str:
    """Функция преобразует строку из формата 2018-07-11T02:26:18.671407 в формат 11.07.2018"""
    date_part = date_str.split("T")[0]  # Разделяем строку по символу "T"
    year, month, day = date_part.split("-")  # Разделяем дату через "-"
    return f"{day}.{month}.{year}"  # Возвращаем строку в нужном формате


# print(get_data("2018-07-11T02:26:18.671407"))

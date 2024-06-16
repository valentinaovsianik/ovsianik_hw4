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

    parts = info.split(maxsplit=1)  # Разбиваем строку по первому пробелу
    if len(parts) != 2:
        raise ValueError("Неверный формат данных")

    account_type = parts[0].lower()  # Берем первый элемент (тип карты или слово "Счет")

    if account_type == "счет":
        account_number = parts[1].strip()  # Берем номер счета и убираем пробелы
        masked_number = get_mask_account(account_number)  # Маскируем номер счета
        return f"{account_type} {masked_number}"  # Возвращаем строку с замаскированным номером счета
    elif account_type in ["visa", "maestro", "mastercard"]:
        card_number = parts[1].replace(" ", "")  # Берем номер карты, убираем пробелы
        if len(card_number) != 16 or not card_number.isdigit():   # Проверяем, что номер карты содержи только цифры
            raise ValueError("Номер карты должен состоять из 16 цифр")
        masked_number = get_mask_card_number(card_number)  # Маскируем номер карты
        return f"{parts[0]} {masked_number}"  # Возвращаем строку с замаскированным номером карты
    else:
        raise ValueError("Нераспознанные данные")


# print(mask_account_card("Visa Platinum 7000 7922 8960 6361"))
# print(mask_account_card("Счет 73654108430135874305"))


def get_data(date_str: str) -> str:
    """Функция преобразует строку из формата 2018-07-11T02:26:18.671407 в формат 11.07.2018"""
    date_part = date_str.split("T")[0]  # Разделяем строку по символу "T"
    year, month, day = date_part.split("-")  # Разделяем дату через "-"
    return f"{day}.{month}.{year}"  # Возвращаем строку в нужном формате


# print(get_data("2018-07-11T02:26:18.671407"))

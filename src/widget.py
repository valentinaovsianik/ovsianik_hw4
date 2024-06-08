def mask_account_card(info: str) -> str:
    """Функция принимает строку с типом карты/счета и номер и возвращает строку с замаскированным номером"""

    def get_mask_card_number(card_number: str) -> str:
        """Функция маскирует номер карты в формате XXXX XX** **** XXXX"""
        card_number = card_number.replace(" ", "")
        if len(card_number) != 16:
            raise ValueError("Номер карты  должен состоять из 16 цифр")
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    def get_mask_account(account_number: str) -> str:
        """Функция маскирует номер счета в формате **XXXX"""
        if len(account_number) < 4:
            raise ValueError("Номер счета должен состоять не менее чем из 4 цифр")
        return f"**{account_number[-4:]}"

    parts = info.split()  # Разбиваем строку  на части
    account_type = parts[0]  # Берем первый элемент (тип карты или слово "Счет")

    if account_type.lower() == "счет":
        account_number = parts[1]  # Берем номер счета
        masked_number = get_mask_account(account_number)  # Маскируем номер счета
        return f"{account_type} {masked_number}"  # Возвращаем строку с замаскированным номером счета
    else:
        card_number = "".join(parts[2:])  # Соединяем все части номера карты
        masked_number = get_mask_card_number(card_number)  # Маскируем номер карты
        return f"{parts[0]} {parts[1]} {masked_number}"  # Возвращаем строку с замаскированным номером карты


def get_data(date_str: str) -> str:
    """Функция преобразует строку из формата 2018-07-11T02:26:18.671407 в формат 11.07.2018"""
    date_part = date_str.split("T")[0]  # Разделяем строку по символу "T"
    year, month, day = date_part.split("-") # Разделяем дату через "-"
    return f"{day}.{month}.{year}" # Возвращаем строку в нужном формате



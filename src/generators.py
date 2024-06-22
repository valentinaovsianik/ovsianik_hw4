def filter_by_currency(transactions, currency):
    """Функция фильтрует операции по указанной валюте"""
    for transaction in transactions:  # Итерация по всем операциям
        if transaction.get("currency") == currency:  # Если валюта соответствует указанной, операция возвращается
            yield transaction


# Функция-генератор принимает список словарей и возвращает описание каждой операции по очереди
def transaction_descriptions(transactions):
    for transaction in transactions:
        description = transaction.get("description")
        yield description


# Генератор номеров банковских карт, который генерирует номера в формате  XXXX XXXX XXXX XXXX
def card_number_generator(start, end):
    for num in range(start, end + 1):
        yield f"{num:016}".replace("000000000000", "0000 0000 0000 ")  # Возвращаем отформатированный номер карты

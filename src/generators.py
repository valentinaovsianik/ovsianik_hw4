def filter_by_currency(transactions, currency):
    """Функция фильтрует операции по указанной валюте"""
    for transaction in transactions:  # Итерация по всем операциям
        if transaction.get("currency") == currency:  # Если валюта соответствует указанной, операция возвращается
            yield transaction

usd_transactions = filter_by_currency(transactions, "USD") # Итератор фильтрует операции по "USD"

for _ in range(2):
    print(next(usd_transactions) [id])) # Извлекаются 2 операции с долларом и печалаются их ID


# Генератор принимает список словарей и возвращает описание каждой операции по очереди
descriptions = (transaction.get("description") for transaction in transactions)

for _ in range(5)
    print(next(descriptions)) # Используется для получения следующего элемента из списка descriptions


import json
import os


def read_transactions(file_path: str) -> list[dict]:
    """Читает данные о финансовых транзакциях из JSON-файла и возвращает список словарей"""
    if not os.path.exists(file_path):  # Проверка на существование файла
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Открытие и чтение JSON-файла
            data = json.load(file)
            if isinstance(data, list):  # Проверяем, является ли содержимое списком
                return data
            else:
                return []
    except (json.JSONDecodeError, OSError):  # Возвращаем пустой список в случае ошибки прич тении или декодировании
        return []


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "../data/operations.json")
    transactions = read_transactions(file_path)
    print(transactions)

import json
import logging
import os
import re
from datetime import datetime

import pandas as pd

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

os.makedirs(log_dir, exist_ok=True)

# Настройка логера
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Настройка обработчика логов
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Путь к csv-файлу
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "transactions.csv")
df = pd.read_csv(csv_file_path)  # Читаем данные из csv

# Создаем xlsx по указанному пути
excel_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "transactions_excel.xlsx")
df.to_excel(excel_file_path, index=False)


def read_transactions(file_path: str) -> list[dict]:
    """Читает данные о финансовых транзакциях из JSON, CSV и XLSX и возвращает список словарей"""
    if not os.path.exists(file_path):  # Проверка на существование файла
        logger.warning(f"Файл {file_path} не существует")
        return []

    file_extension = os.path.splitext(file_path)[1].lower()  # Определяем расширение файла

    try:
        if file_extension == ".json":
            with open(file_path, "r", encoding="utf-8") as file:  # Открытие и чтение JSON-файла
                data = json.load(file)
                if isinstance(data, list):  # Проверяем, является ли содержимое списком
                    logger.info(f"Данные из файла {file_path} прочитаны успешно")
                    return data
                else:
                    logging.warning(f"Файл {file_path} не содержит список транзакций")
                    return []

        elif file_extension == ".csv":
            data = pd.read_csv(file_path, sep=";")  # Читаем csv-файл
            logger.info(f"Данные из файла {file_path} прочитаны успешно")
            return data.to_dict(orient="records")

        elif file_extension == ".xlsx":
            data = pd.read_excel(file_path)  # Читаем xlsx-файл
            logger.info(f"Данные из файла {file_path} прочитаны успешно")
            return data.to_dict(orient="records")
        else:
            logging.warning(f"Неподдерживаемый формат файла: {file_extension}")
            return []

    except (
        json.JSONDecodeError,
        OSError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ) as e:  # Возвращаем пустой список если ошибка при чтении или декодировании
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def search_transactions(transactions: list[dict], search_string: str) ->list[dict]:
    """Ищет транзакции, в описании которых есть заданная строка поиска"""

    search_pattern = re.compile(re.escape(search_string), re.IGNORECASE) # Компилируем регулярное выражение для строки поиска

    matched_transactions = [] # Создаем список для хранения найденных транзакций

    for transaction in transactions: # Проверяем, есть ли описание в транзакции и соответствует ли оно строке поиска
        if isinstance(transaction.get("description"), str) and search_pattern.search(transaction["description"]):
            matched_transactions.append(transaction)

    return matched_transactions


def categorize_transactions(transactions: list[dict], categories: list) -> dict:
    """Разбивает транзакции по категориям в зависимости от описания и считает количество транзакций в каждой категории"""
    category_counts = {category: 0 for category in  categories} # Создаем словарь для каждой категории транзакций

    for transaction in transactions:
        description = transaction.get("description", "") # Получаем описание операции

        if description in category_counts: # Если описание соответствует одной из категорий
            category_counts[description] += 1 # увеличиваем счетчик

    return category_counts


if __name__ == "__main__":
    transactions = [
        {"id": 650703, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z", "amount": 16210, "currency_name": "Sol",
         "currency_code": "PEN", "from": "Счет 58803664561298323391", "to": "Счет 39745660563456619397",
         "description": "Перевод организации"},
        {"id": 3598919, "state": "EXECUTED", "date": "2020-12-06T23:00:58Z", "amount": 29740, "currency_name": "Peso",
         "currency_code": "COP", "from": "Discover 3172601889670065", "to": "Discover 0720428384694643",
         "description": "Перевод с карты на карту"},
        {"id": 593027, "state": "CANCELED", "date": "2023-07-22T05:02:01Z", "amount": 30368,
         "currency_name": "Shilling", "currency_code": "TZS", "from": "Visa 1959232722494097",
         "to": "Visa 6804119550473710", "description": "Перевод с карты на карту"},
        {"id": 366176, "state": "EXECUTED", "date": "2020-08-02T09:35:18Z", "amount": 29482, "currency_name": "Rupiah",
         "currency_code": "IDR", "from": "Discover 0325955596714937", "to": "Visa 3820488829287420",
         "description": "Перевод с карты на карту"},
        {"id": 5380041, "state": "CANCELED", "date": "2021-02-01T11:54:58Z", "amount": 23789, "currency_name": "Peso",
         "currency_code": "UYU", "from": "", "to": "Счет 23294994494356835683", "description": "Открытие вклада"}
        ]

    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
    result = categorize_transactions(transactions, categories)
    print(result)


    # file_path = os.path.join(os.path.dirname(__file__), "..", "data", "transactions.csv")
    # search_string = "Перевод с карты на карту"
    #
    # transactions = read_transactions(file_path)
    # result = search_transactions(transactions, search_string)
    #
    # for transaction in result:
    #     print(transaction)

    # file_path_json = os.path.join(os.path.dirname(__file__), "../data/operations.json")
    # file_path_csv = os.path.join(os.path.dirname(__file__), "../data/transactions.csv")
    # file_path_xlsx = os.path.join(os.path.dirname(__file__), "../data/transactions_excel.xlsx")
    #
    # transactions_json = read_transactions(file_path_json)
    # transactions_csv = read_transactions(file_path_csv)
    # transactions_xlsx = read_transactions(file_path_xlsx)
    #
    # print("JSON Transactions", transactions_json)
    # print("CSV Transactions", transactions_csv)
    # print("XLSX Transactions", transactions_xlsx)

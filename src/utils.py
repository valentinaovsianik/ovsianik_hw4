import json
import logging
import os
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


if __name__ == "__main__":
    file_path_json = os.path.join(os.path.dirname(__file__), "../data/operations.json")
    file_path_csv = os.path.join(os.path.dirname(__file__), "../data/transactions.csv")
    file_path_xlsx = os.path.join(os.path.dirname(__file__), "../data/transactions_excel.xlsx")

    transactions_json = read_transactions(file_path_json)
    transactions_csv = read_transactions(file_path_csv)
    transactions_xlsx = read_transactions(file_path_xlsx)

    print("JSON Transactions", transactions_json)
    print("CSV Transactions", transactions_csv)
    print("XLSX Transactions", transactions_xlsx)

import json
import logging
import os
from datetime import datetime

log_directory = "C:\\Users\\Dell\\PycharmProjects\\ovsianik_hw4\\logs\\"
module_name = "utils"

#  Формируем имя файла
log_filename = f"{log_directory}/{module_name}_{datetime.now().strftime('%Y-%m-%d')}.log"

#  Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler(log_filename, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

#  Задаем формат сообщений
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

#  Создаем логер и добавляем обработчик к нему
logger = logging.getLogger(module_name)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def read_transactions(file_path: str) -> list[dict]:
    """Читает данные о финансовых транзакциях из JSON-файла и возвращает список словарей"""
    if not os.path.exists(file_path):  # Проверка на существование файла
        logger.warning(f"Файл {file_path} не существует")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Открытие и чтение JSON-файла
            data = json.load(file)
            if isinstance(data, list):  # Проверяем, является ли содержимое списком
                logger.info(f"Данные из файла {file_path} прочитаны успешно")
                return data
            else:
                logging.warning(f"Файл {file_path} не содержит список транзакций")
                return []
    except (json.JSONDecodeError, OSError) as e:  # Возвращаем пустой список если ошибка при чтении или декодировании
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")

        return []


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "../data/operations.json")
    transactions = read_transactions(file_path)
    print(transactions)

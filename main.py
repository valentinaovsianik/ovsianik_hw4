import csv
import json
import os
from datetime import datetime
from functools import wraps

import pandas as pd

from src.external_api import convert_currency
from src.generators import filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import categorize_transactions, read_transactions, search_transactions
from src.widget import get_data, mask_account_card


def main():
    """Объединяет все функции проекта"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню: ")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    base_dir = os.path.dirname(os.path.abspath(__file__)) # Определяем базовый путь к папке data
    data_dir = os.path.join(base_dir, "data")

    user_choice = input("Пользователь: ")

    if user_choice == "1":
        file_path = os.path.join(data_dir, "operations.json")
        print("Для обработки выбран JSON-файл.")
    elif user_choice == "2":
        file_path = os.path.join(os.path.dirname(__file__), "../data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    elif user_choice == "3":
        file_path = os.path.join(os.path.dirname(__file__), "../data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")
        return

    transactions = read_transactions(file_path)  # Чтение транзакций из выбранного файла

    if not transactions:
        print("Не удалось прочитать транзакции. Завершение программы.")
        return

    print("Доступные для фильтровки статусы:")
    valid_statuses = set()
    for transaction in transactions:
        if "state" in transaction:
            valid_statuses.add(transaction["state"])

    statuses_str = ", ".join(valid_statuses)
    print(statuses_str)

    status = input("Введите статус, по которому необходимо выполнить фильтрацию. \nПользователь: ").strip().upper()

    filtered_transactions = filter_by_state(transactions, status)  # Фильтруем транзакции по статусу
    if not filtered_transactions:
        print(f"Статус операции '{status}' недоступен.")
        return

    print(f"Операции отфильтрованы по статусу '{status}'")

    # Сортировка транзакций по дате при необходимости
    sort_choice = input("Отсортировать операции по дате? Да/Нет" "\nПользователь: ").strip().lower()
    if sort_choice == "да":
        sort_order = input("Отсортировать по возрастанию или по убыванию?\n ").strip().lower()
        ascending = sort_order == "по возрастанию"

        filtered_transactions = sort_by_date(filtered_transactions, reverse=not ascending)

    # Вывод только рублевых транзакций при необходимости
    currency_choice = input("Выводить только рублевые транзакции? Да/Нет" "\nПользователь: ").strip().lower()
    if currency_choice == "да":
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")
    else:  # Конвертация валюты для операций не в рублях
        filtered_transactions = [convert_currency(transaction) for transaction in filtered_transactions]

    # Фильтрация транзакций по слову в описании при необходимости
    search_choice = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if search_choice == "да":
        search_string = input("Введите слово для поиска в описании транзакций" "\nПользователь: ")
        filtered_transactions = search_transactions(filtered_transactions, search_string)

    filtered_transactions = list(filtered_transactions)  # Преобразование генератора в список

    print("Распечатываю итоговый список транзакций...")

    if filtered_transactions:
        print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")
        for transaction in filtered_transactions:
            # Форматирование вывода информации о транзакции
            date = get_data(transaction.get("date"))  # Преобразование даты
            description = next(transaction_descriptions([transaction]))  # Получение описания транзакции
            currency = transaction.get("currency", "RUB")

            if "from" in transaction and "to" in transaction:
                from_account = transaction["from"]
                to_account = transaction["to"]
                masked_from_account = get_mask_account(from_account)
                masked_to_account = get_mask_account(to_account)
                amount = transaction.get("amount")
                print(
                    f"{date} {description}\n{masked_from_account} -> {masked_to_account}\nСумма: {amount} {currency}\n"
                )
            else:
                account = transaction.get("account", "")
                masked_account = get_mask_account(account)
                amount = transaction.get("amount")
                print(f"{date} {description}\nСчет {masked_account}\nСумма: {amount} {currency}\n")

            # Категоризация транзакций и вывод количества транзакций по категориям
            categories = ["EXECUTED", "CANCELED", "PENDING"]
            category_counts = categorize_transactions(filtered_transactions, categories)
            print("Количество транзакций по категориям:")
            for category, count in category_counts.items():
                print(f"{category}: {count}")
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()

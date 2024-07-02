import requests
import os
from dotenv import load_dotenv

load_dotenv()


def convert_currency(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли с использованием внешнего API"""

    api_key = os.getenv("API_KEY")

    try:
        amount = transaction["amount"]
        currency = transaction["currency"]

        if currency == "RUB":
            return amount

        api_url = f"https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": api_key}

        response = requests.get(api_url, headers=headers) # Отправляем get-запрос к API
        response.raise_for_status() # Проверка успешности запроса

        data = response.json() # Парсим JSON-ответ

        if currency == "USD": # Получаем курс  обмена валют к RUB
            exchange_rate = data["rates"]["RUB"] / data["rates"]["USD"]
        elif currency == "EUR":
            exchange_rate = data["rates"]["RUB"] / data["rates"]["EUR"]
        else:
            return amount # Возвращаем исходную сумму, если валюта не доллары и евро

        converted_amount = amount * exchange_rate # Конвертируем сумму в рубли
        return converted_amount

    # Обработка исключений
    except requests.exceptions.RequestException as e: # "Ловим" проблемы, связанные с запросом
        print(f"Error fetching exchange rates: {e}")
        return None
    except (KeyError, ValueError) as e: # "Ловим" проблемы, связанные с неправильной структурой/некорректными значениями JSON-ответа
        print(f"Error parsing JSON response: {e}")
        return None

if __name__ == "__main__":
    transaction = {"amount": 100, "currency": "USD"}
    converted_amount = convert_currency(transaction)

    if converted_amount is not None:
        print(f"{converted_amount} RUB")
    else:
        print(f"Не удалось выполнить конвертацию")



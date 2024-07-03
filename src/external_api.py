import requests
import os
from dotenv import load_dotenv

load_dotenv()


def convert_currency(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли с использованием внешнего API"""

    api_key = os.getenv("API_KEY")  # Получаем API-ключ

    try:  # Извлекаем сумму и валюту из переданного словаря
        amount = transaction["amount"]
        currency = transaction["currency"]

        if currency == "RUB":  # Если валюта транзакции в рублях, возвращаем сумму
            return amount

        api_url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": api_key}

        response = requests.get(api_url, headers=headers)  # Отправляем get-запрос к API
        response.raise_for_status()  # Проверка успешности запроса

        data = response.json()  # Парсим JSON-ответ

        converted_amount = data["result"]  # Получаем конвертируемую сумму в рублях
        return converted_amount

    # Обработка исключений
    except requests.exceptions.RequestException as e:  # "Ловим" проблемы, связанные с запросом
        print(f"Error fetching exchange rates: {e}")
        return None
    except (KeyError, ValueError) as e:  # "Ловим" проблемы, связанные с JSON-ответом
        print(f"Error parsing JSON response: {e}")
        return None


if __name__ == "__main__":
    transaction = {"amount": 100, "currency": "USD"}
    converted_amount = convert_currency(transaction)

    if converted_amount is not None:
        print(f"{converted_amount} RUB")
    else:
        print("Не удалось выполнить конвертацию")

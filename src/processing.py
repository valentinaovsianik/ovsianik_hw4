def filter_by_state(data: list, state="EXECUTED": str) -> list:
    """Функция фильтрует список словарей по значению ключа state"""
    filtered_data = []

    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)

    return  filtered_data

# Примеры
# data = {"id": 41428829, "state": "EXECUTED", "date": "2019"-07-03T18:35:29.512364"}
#        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}

# Выход функции
# print(filter_by_state(data))
# print(filter_by_state(data, "CANCELED"))
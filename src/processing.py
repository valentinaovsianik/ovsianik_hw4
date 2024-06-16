def filter_by_state(data: list, state: str = "EXECUTED") -> list:
    """Функция фильтрует список словарей по значению ключа state"""
    filtered_data = []

    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)

    return filtered_data


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Функция сортирует список словарей по дате"""
    sorted_data = sorted(data, key=lambda x: x["date"], reverse=reverse)  # Устанавливаем порядок сортировки
    return sorted_data


# data = [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}]

# Выход функции фильтрации
# print(filter_by_state(data))
# print(filter_by_state(data, "CANCELED"))

# Сортировка по убыванию
# print(sort_by_date(data))

# Сортировка по возрастанию
# print(sort_by_date(data, reverse=False))

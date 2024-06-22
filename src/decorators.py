from functools import wraps


def log(filename=None):
    """Декоратор логирует вызов функции и ее результат в файл (если аргумент задан) или в консоль (если не задан)"""

    def decorator(func):
        """Принимает функцию, которую нужно обернуть логированием"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Внутри функции происходит обертка вызова функции func"""
            try:  # Пытаемся выполнить функцию func с переданными аргументами
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"  # Формируем сообщение об успешном выполнении
                if filename:  # Если filename указан
                    with open(filename, "a") as f:  # Открываем файл для добавления данных
                        f.write(log_message + "\n")  # Записываем сообщение об успешном выполнении
                else:  # Если filename не указан, выводим сообщение об успешном выполнении в консоль
                    print(log_message)
                return result  # Возвращаем результат выполнения функции func
            except Exception as e:  # Если при выполнении функции возникает исключение
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"  # Cообщение об ошибке
                )
                if filename:  # Если filename указан
                    with open(filename, "a") as f:
                        f.write(error_message + "\n")  # Записываем сообщение об ошибке
                else:  # Если filename не указан, выводим сообщение об ошибке в консоль
                    print(error_message)
                raise

        return wrapper  # Возвращаем функцию-обертку wrapper

    return decorator  # Возвращаем функцию-декоратор


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)

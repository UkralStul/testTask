def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов аргументов
        annotations = func.__annotations__
        param_names = list(annotations.keys())[:-1]  # Исключаем return

        # Проверяем количество аргументов
        if len(args) != len(param_names):
            raise TypeError("Количество аргументов не совпадает с сигнатурой функции.")

        # Проверяем соответствие типов
        for arg, param_name in zip(args, param_names): # Объединяем аргументы и их типы в кортеж
            expected_type = annotations[param_name]
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Аргумент '{param_name}' имеет некорректный тип: ожидался {expected_type}, получен {type(arg)}",
                    )

        return func(*args, **kwargs)

    return wrapper

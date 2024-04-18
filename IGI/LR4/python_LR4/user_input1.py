def choose_way():
    """
    Select input method.

    :return: selection number
    """
    while True:
        try:
            print("Выберите способ инициализации:")
            print("1. Ввод с клавиатуры.")
            print("2. Автоматическое заполнение.")
            choose = int(input())
            if choose != 1 and choose != 2:
                raise ValueError("Неверный ввод.")
            return choose
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
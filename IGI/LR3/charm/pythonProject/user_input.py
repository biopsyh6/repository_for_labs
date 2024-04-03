def choose_task():
    """
    Choose task number.

    :return: task number
    """
    while True:
        try:
            print("Выберите задание 1-5 или 0 для выхода из программы:")
            task = int(input())
            return task
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
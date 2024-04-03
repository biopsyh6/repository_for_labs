def input_number():
    """
    Enter integer number.

    :return: number
    """
    while True:
        try:
            print("Введите целое число: ")
            number = int(input())
            return number
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
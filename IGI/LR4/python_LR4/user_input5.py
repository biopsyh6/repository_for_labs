def input_number():
    """
    Enter integer number.

    :return: number
    """
    while True:
        try:
            number = int(input())
            if number > 0:
                return number
            else:
                print("Ошибка. Введите положительное значение.")
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
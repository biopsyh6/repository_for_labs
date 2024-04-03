def input_value():
    """
    Enter the value in degrees.

    :return: value
    """
    while True:
        try:
            print("Введите в градусах значение: ")
            x = float(input())
            if x < 0 or x > 360:
                raise ValueError("Введите корректное значение")
            return x
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")


def input_error():
    """
    Enter error in calculations.

    :return: error
    """
    while True:
        try:
            print("Введите погрешность: ")
            eps = float(input())
            if eps < 0:
                raise ValueError("Введите корректное значение")
            return eps
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
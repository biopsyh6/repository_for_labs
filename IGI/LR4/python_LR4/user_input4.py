def input_number():
    """
    Enter integer number.

    :return: number
    """
    while True:
        try:
            print("Введите радиус: ")
            number = int(input())
            if number > 0:
                return number
            else:
                print("Ошибка. Введите положительное значение.")
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")

def input_color():
    while True:
        color = input("Введите цвет (red, green, yellow, orange, purple, gray): ")
        if color not in ["red", "green", "yellow", "orange", "purple", "gray"]:
            print("Введите корректный цвет.")
        else:
            break
    return color
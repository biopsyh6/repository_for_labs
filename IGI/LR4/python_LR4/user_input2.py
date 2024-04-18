def input_number():
    """
    Enter integer number.

    :return: number
    """
    while True:
        try:
            print("Введите длину слова для замены на $: ")
            number = int(input())
            return number
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
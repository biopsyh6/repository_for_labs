import random


def get_list_size():
    """
    Get list size.

    :return: size
    """
    while True:
        try:
            print("Введите размерность списка: ")
            size = int(input())
            if size < 0:
                raise ValueError("Размер списка не может быть отрицательным")
            return size
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")


def choose_way():
    """
    Select input method.

    :return: selection number
    """
    while True:
        try:
            print("Выберите способ инициализации списка:")
            print("1. Ввод с клавиатуры.")
            print("2. Ввод с помощью генератора.")
            choose = int(input())
            if choose != 1 and choose != 2:
                raise ValueError("Неверный ввод.")
            return choose
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")


def input_elements(size):
    """
    Enter list elements.

    :param size: list size
    :return: float list
    """
    float_list = []
    print("Введите элементы списка: ")
    i = 0
    while i < size:
        try:
            number = float(input())
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
        else:
            float_list.append(number)
            i += 1
    return float_list


def generate_random_list(length):
    """
    Generate random list.

    :param length: list size
    :return: generator
    """
    return (random.uniform(-100.0, 100.0) for _ in range(length))


def initialize_list_generator(generator_func):
    """
    Return list generator.

    :param generator_func: generator function
    :return: list
    """
    return list(generator_func)



import numpy as np


class TestNumPy:
    @staticmethod
    def test():
        """
        Test NumPy methods
        :return:
        """
        lst = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        arr_np = np.array(lst)
        print("Тест функций numPy")
        print("Создание массива через np.array: ")
        print(arr_np)
        print("Индекс и срез: ")
        print(arr_np[1:5])
        print("Массив + 3: ")
        arr_np = np.add(arr_np, 3)
        print(arr_np)
        print("Массив * -4: ")
        arr_np = np.multiply(arr_np, -4)
        print(arr_np)
        print("Среднее арифметическое mean(): ")
        print(np.mean(arr_np))
        print("Корреляция: ")
        print(np.corrcoef(arr_np))
        print("Дисперсия: ")
        print(np.var(arr_np))
        print("Стандартное отклонение: ")
        print(f"{np.std(arr_np):.5f}")

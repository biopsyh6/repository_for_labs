import numpy as np
import user_input5
from Tasks.Task5.testNumPy import TestNumPy
class Task5:
    def __init__(self):
        self.matrix = None
        self.rows = None
        self.columns = None

    def get_matrix(self):
        """
        Get matrix
        :return: matrix
        """
        return self.matrix

    def solve(self):
        """
        Solve this task
        :return:
        """
        TestNumPy.test()
        self.create_matrix()
        print(self.get_matrix())
        column, min_summ = self.find_column_with_min_sum()
        print(f"Столбец с наименьшей суммой элементов: {column}.")
        print(f"Сумма элементов {min_summ}.")
        print(f"Значение медианы этого столбца: {np.median(column)}.")
        median = self.get_median(column)
        print(f"Значение медианы через формулу: {median}.")

    def create_matrix(self):
        """
        Get matrix with random initialization
        :return:
        """
        print("Введите количество строк: ")
        self.rows = user_input5.input_number()
        print("Введите количество столбцов: ")
        self.columns = user_input5.input_number()
        self.matrix = np.random.randint(-1000, 1000, (self.rows, self.columns))

    def find_column_with_min_sum(self):
        """
        Get column with minimal sum
        :return: column, min_sum
        """
        min_summ = 0
        column = None
        for i in range(self.columns):
            summ = sum(self.matrix[:, i])
            if summ < min_summ or min_summ == 0:
                min_summ = summ
                column_number = i
                column = self.matrix[:, i]
        return column, min_summ

    @staticmethod
    def get_median(column):
        """
        Get median
        :param column:
        :return: median
        """
        column.sort()
        print(column)
        length = len(column)
        if length % 2 != 0:
            return column[length // 2]
        else:
            median = (column[length // 2 - 1] + column[length // 2]) / 2
            return median

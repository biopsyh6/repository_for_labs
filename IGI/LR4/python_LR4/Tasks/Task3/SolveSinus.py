import numpy as np
import matplotlib.pyplot as plt
import math


class SolveSin:
    def __init__(self):
        self.__data = np.array([])

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    def calculate_sum(self, x, eps):
        """
          Solve sinus.

          :param x: value in radians
          :param eps: calculation accuracy
          :return: sinus result, number of series members
          """
        S = 0  # Сумма ряда на старте
        i = 1  # Порядковый номер слагаемого в ряду Тейлора
        q = x
        itetations = 0
        series_elements = np.array([])
        # Пока очередное слагаемое больше погрешности
        while abs(q) > eps and itetations <= 500:
            series_elements = np.append(series_elements, q)
            S = S + q
            q = q * (-1) * (x * x) / ((2 * i + 1) * (2 * i))
            i += 1
            itetations += 1
        self.data = series_elements
        return S, i

    def plot(self, x_min, x_max, step, path_to_file=None):
        """
        Draws graph
        :param x_min:
        :param x_max:
        :param step:
        :param path_to_file:
        :return: plot
        """
        x = np.arange(x_min, x_max, step)
        y_series = [self.calculate_sum(xi, 0.001)[0] for xi in x]
        y_function = [math.sin(xi) for xi in x]

        fig, ax = plt.subplots()
        ax.grid(True)

        plt.plot(x, y_series, color="green")
        plt.plot(x, y_function, color="red")
        plt.xlabel('x')
        plt.ylabel('sin(x)')
        plt.legend(['math.sin', 'taylor series for sin'])

        if path_to_file:
            try:
                plt.savefig(path_to_file)
            except ValueError as e:
                print(f"Ошибка {e}. Некорректный путь.")

        plt.show()

    def get_average(self):
        """
        Calculate average of elements
        :return: average
        """
        return np.average(self.__data)

    def get_median(self):
        """
        Calculate median
        :return: median
        """
        return np.median(self.__data)

    def get_mode(self):
        """
        Calculate mode of elements
        :return: mode
        """
        vals, counts = np.unique(self.__data, return_counts=True)
        mode_value = np.argwhere(counts == np.max(counts))
        return vals[mode_value]

    def get_dispersion(self):
        """
        Calculate dispersion of elements
        :return: dispersion
        """
        return np.var(self.__data)

    def get_average_square_deviation(self):
        """
        Calculate average square deviation of elements
        :return: std
        """
        return np.std(self.__data)

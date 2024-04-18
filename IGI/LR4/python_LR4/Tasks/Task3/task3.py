import math
import Tasks.Task3.SolveSinus, user_input3
from tabulate import tabulate

from Tasks.Task3 import SolveSinus


class Task3:
    @staticmethod
    def solve():
        """
        Solve this task
        :return:
        """
        table = []
        solve_sin = SolveSinus.SolveSin()
        x = user_input3.input_value()
        x_radians = x / 180 * math.pi
        eps = user_input3.input_error()
        result, number = solve_sin.calculate_sum(x_radians, eps)
        true_result = math.sin(x_radians)
        table.append([x, number, result, true_result, eps])
        print(tabulate(table, headers=["x", "n", "F(x)", "Math F(x)", "eps"]))

        print(f"Data: {solve_sin.data}")
        print(f"Average: {solve_sin.get_average()}")
        print(f"Median: {solve_sin.get_median()}")
        print(f"Mode: {solve_sin.get_mode()}")
        print(f"Dispersion {solve_sin.get_dispersion()}")
        print(f"Average square deviation: {solve_sin.get_average_square_deviation()}")

        solve_sin.plot(-2, 2, 0.1, 'Task3plot.png')

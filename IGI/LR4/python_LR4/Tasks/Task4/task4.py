from Tasks.Task4.CircumscribedTriangle import CircumscribedTriangle
from Tasks.Task4.figure_color import FigureColor
import user_input4
class Task4:
    @staticmethod
    def solve():
        """
        Solve this task
        :return:
        """
        try:
            r = user_input4.input_number()
            color = user_input4.input_color()
            text = input("Введите текст: ")
            shape_color = FigureColor(color)
            triangle = CircumscribedTriangle(r, shape_color, text)
            triangle.draw()
            triangle.save()
            print(str(triangle))
        except ValueError as e:
            print(f"Ошибка: {e}")

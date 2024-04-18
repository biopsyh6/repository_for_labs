import math
from PIL import Image, ImageDraw, ImageFont
from Tasks.Task4.geometric_figure import GeometricFigure
from Tasks.Task4.figure_color import FigureColor


class CircumscribedTriangle(GeometricFigure, FigureColor):
    def __init__(self, r, color: str, text=""):
        super().__init__(color)
        self.r = r
        self.color = FigureColor(color)
        self.triangle_side = (6 * self.r) / math.sqrt(3)
        self.text = text
        self.image = Image.new('RGB', (1000, 1000), 'white')

    def count_square(self):
        """
        Get area
        :return: area
        """
        return ((self.triangle_side * 3) / 2) * self.r

    def __str__(self):
        return "{0} shape, color: {1}, side size: {2}, area: {3}".format(self.__class__.__name__, self.color.__str__(),
                                                                         self.triangle_side, self.count_square())

    def draw(self):
        """
        Draw triangle
        :return:
        """
        image = Image.new('RGB', (1000, 1000), 'white')
        draw = ImageDraw.Draw(image) #Создаем объект ImageDraw
        font = None
        if __name__ != "__main__":
            font = ImageFont.truetype('arial.ttf', size=18)
        # draw.ellipse((10, 10, 2 * self.__r + 10, 2 * self.__r + 10), fill="white", outline="black", width=4)

        center_x = self.r + 10
        center_y = self.r + 10
        center = self.r + 10
        radius = self.r
        radius2 = 2 * self.r
        color = self.color.__str__()
        angle = math.pi / 6  # 30 градусов в радианах
        x1 = center_x + radius * math.cos(angle)
        y1 = center_y - radius * math.sin(angle)
        x2 = center_x + radius * math.cos(angle + 2 * math.pi / 3)
        y2 = center_y - radius * math.sin(angle + 2 * math.pi / 3)
        x3 = center_x + radius * math.cos(angle - 2 * math.pi / 3)
        y3 = center_y - radius * math.sin(angle - 2 * math.pi / 3)

        draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=str(color), outline="black")
        ellipse = (center_x - radius / 2, center_y - radius / 2, center_x + radius / 2, center_y + radius / 2)
        draw.ellipse(ellipse, fill="blue", outline="black")
        draw.text((center, center + 500), self.text, font=font, fill="black")

        image.show()
        self.image = image

    def save(self):
        """
        Save in file
        :return:
        """
        self.image.save("Task4.jpg")



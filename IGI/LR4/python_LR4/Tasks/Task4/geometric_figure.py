from abc import ABC, abstractmethod


class GeometricFigure(ABC):
    @abstractmethod
    def count_square(self):
        pass

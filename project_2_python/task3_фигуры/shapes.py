from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def compare_area(self, other: 'Shape') -> str:
        if self.area() > other.area(): return "Больше"
        elif self.area() < other.area(): return "Меньше"
        return "Равно"
    
    def compare_perimeter(self, other: 'Shape') -> str:
        if self.perimeter() > other.perimeter(): return "Больше"
        elif self.perimeter() < other.perimeter(): return "Меньше"
        return "Равно"
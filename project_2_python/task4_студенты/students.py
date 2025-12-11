class Student:
    def __init__(self, full_name: str, age: int, group: str, avg_score: float):
        self.full_name = full_name
        self.age = age
        self.group = group
        self.avg_score = avg_score
    
    def display_info(self):
        print(f"ФИО: {self.full_name}, Возраст: {self.age}")
    
    def get_scholarship(self) -> int:
        if self.avg_score == 5: return 6000
        elif self.avg_score < 5: return 4000
        return 0
    
    def compare_scholarship(self, other) -> str:
        diff = self.get_scholarship() - other.get_scholarship()
        return "Больше" if diff > 0 else "Меньше" if diff < 0 else "Равно"

class Postgraduate(Student):
    def __init__(self, full_name: str, age: int, group: str, avg_score: float, thesis: str):
        super().__init__(full_name, age, group, avg_score)
        self.thesis = thesis
    
    def get_scholarship(self) -> int:
        if self.avg_score == 5: return 8000
        elif self.avg_score < 5: return 6000
        return 0
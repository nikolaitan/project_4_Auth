from pydantic import BaseModel
from typing import Optional, List

# Базовая модель группы (общие поля)
class GroupBase(BaseModel):
    name: str  # Название группы

# Модель для создания группы (наследует GroupBase)
class GroupCreate(GroupBase):
    pass

# Модель ответа группы (с ID и списком студентов)
class Group(GroupBase):
    id: int  # ID группы
    students: List["Student"] = []  # Список студентов группы (по умолчанию пустой)

    class Config:
        orm_mode = True  # Поддержка преобразования из ORM-моделей

# Базовая модель студента (общие поля)
class StudentBase(BaseModel):
    name: str  # Имя студента
    group_id: Optional[int] = None  # ID группы (опционально)

# Модель для создания студента
class StudentCreate(StudentBase):
    pass

# Модель ответа студента (с ID)
class Student(StudentBase):
    id: int  # ID студента

    class Config:
        orm_mode = True  # Поддержка ORM-моделей

# Решение циклической ссылки (Group ссылается на Student, и наоборот)
Group.update_forward_refs()
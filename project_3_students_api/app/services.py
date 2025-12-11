from sqlalchemy.orm import Session
from . import models, schemas  # Импорт моделей и схем

# ------------------------------
# Сервисы для групп
# ------------------------------
def create_group(db: Session, group: schemas.GroupCreate):
    """Создать новую группу"""
    db_group = models.Group(name=group.name)  # Создание экземпляра модели
    db.add(db_group)  # Добавление в сессию
    db.commit()  # Фиксация транзакции
    db.refresh(db_group)  # Обновление объекта (получение ID из БД)
    return db_group

def get_group(db: Session, group_id: int):
    """Получить группу по ID"""
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    """Получить список групп (с пагинацией)"""
    return db.query(models.Group).offset(skip).limit(limit).all()

def delete_group(db: Session, group_id: int):
    """Удалить группу"""
    db_group = get_group(db, group_id)
    if not db_group:
        return None  # Группа не найдена
    db.delete(db_group)
    db.commit()
    return db_group

# ------------------------------
# Сервисы для студентов
# ------------------------------
def create_student(db: Session, student: schemas.StudentCreate):
    """Создать нового студента"""
    db_student = models.Student(**student.dict())  # Распаковка схемы в поля модели
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    """Получить студента по ID"""
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    """Получить список студентов (с пагинацией)"""
    return db.query(models.Student).offset(skip).limit(limit).all()

def delete_student(db: Session, student_id: int):
    """Удалить студента"""
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student

# ------------------------------
# Сервисы для членства в группах
# ------------------------------
def add_student_to_group(db: Session, student_id: int, group_id: int):
    """Добавить студента в группу"""
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    if not student or not group:
        return None  # Студент или группа не найдены
    student.group_id = group_id  # Обновление group_id студента
    db.commit()
    db.refresh(student)
    return student

def remove_student_from_group(db: Session, student_id: int):
    """Удалить студента из группы (сделать без группы)"""
    student = get_student(db, student_id)
    if not student:
        return None
    student.group_id = None
    db.commit()
    db.refresh(student)
    return student

def get_students_in_group(db: Session, group_id: int):
    """Получить всех студентов группы"""
    group = get_group(db, group_id)
    if not group:
        return None
    return group.students  # Получение списка студентов через связь

def transfer_student(db: Session, student_id: int, new_group_id: int):
    """Перевести студента в другую группу"""
    return add_student_to_group(db, student_id, new_group_id)  # Переиспользование логики
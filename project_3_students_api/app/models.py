from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  # Определение связей
from .database import Base

# Модель группы
class Group(Base):
    __tablename__ = "groups"  # Имя таблицы в БД
    id = Column(Integer, primary_key=True, index=True)  # PK ID
    name = Column(String, unique=True, index=True)  # Название группы (уникальное)
    
    # Связь: группа содержит много студентов (обратная ссылка)
    students = relationship("Student", back_populates="group")

# Модель студента
class Student(Base):
    __tablename__ = "students"  # Имя таблицы в БД
    id = Column(Integer, primary_key=True, index=True)  # PK ID
    name = Column(String, index=True)  # Имя студента
    group_id = Column(Integer, ForeignKey("groups.id"))  # FK (связь с группой)
    
    # Связь: студент принадлежит одной группе (прямая ссылка)
    group = relationship("Group", back_populates="students")
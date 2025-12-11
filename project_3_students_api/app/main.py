from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, services
from .database import SessionLocal, engine

# Создание таблиц в БД (при первом запуске)
models.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI-приложения
app = FastAPI(title="API системы управления студентами", version="1.0.0")

# Зависимость: получение сессии БД (автоматическое закрытие)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# Эндпоинты для групп
# ------------------------------
@app.post("/groups/", response_model=schemas.Group, tags=["Группы"])
def create_group_api(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """Создать группу"""
    return services.create_group(db, group)

@app.get("/groups/{group_id}", response_model=schemas.Group, tags=["Группы"])
def get_group_api(group_id: int, db: Session = Depends(get_db)):
    """Получить информацию о группе по ID"""
    db_group = services.get_group(db, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@app.get("/groups/", response_model=list[schemas.Group], tags=["Группы"])
def get_groups_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список групп"""
    return services.get_groups(db, skip, limit)

@app.delete("/groups/{group_id}", response_model=schemas.Group, tags=["Группы"])
def delete_group_api(group_id: int, db: Session = Depends(get_db)):
    """Удалить группу"""
    db_group = services.delete_group(db, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

# ------------------------------
# Эндпоинты для студентов
# ------------------------------
@app.post("/students/", response_model=schemas.Student, tags=["Студенты"])
def create_student_api(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Создать студента"""
    return services.create_student(db, student)

@app.get("/students/{student_id}", response_model=schemas.Student, tags=["Студенты"])
def get_student_api(student_id: int, db: Session = Depends(get_db)):
    """Получить информацию о студенте по ID"""
    db_student = services.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@app.get("/students/", response_model=list[schemas.Student], tags=["Студенты"])
def get_students_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список студентов"""
    return services.get_students(db, skip, limit)

@app.delete("/students/{student_id}", response_model=schemas.Student, tags=["Студенты"])
def delete_student_api(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента"""
    db_student = services.delete_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

# ------------------------------
# Эндпоинты для членства в группах
# ------------------------------
@app.post("/students/{student_id}/group/{group_id}", response_model=schemas.Student, tags=["Членство в группах"])
def add_to_group_api(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """Добавить студента в группу"""
    result = services.add_student_to_group(db, student_id, group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Студент или группа не найдены")
    return result

@app.delete("/students/{student_id}/group", response_model=schemas.Student, tags=["Членство в группах"])
def remove_from_group_api(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента из группы"""
    result = services.remove_student_from_group(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return result

@app.get("/groups/{group_id}/students", response_model=list[schemas.Student], tags=["Членство в группах"])
def get_students_in_group_api(group_id: int, db: Session = Depends(get_db)):
    """Получить всех студентов группы"""
    result = services.get_students_in_group(db, group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return result

@app.post("/students/{student_id}/transfer/{new_group_id}", response_model=schemas.Student, tags=["Членство в группах"])
def transfer_student_api(student_id: int, new_group_id: int, db: Session = Depends(get_db)):
    """Перевести студента в другую группу"""
    result = services.transfer_student(db, student_id, new_group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Студент или новая группа не найдены")
    return result
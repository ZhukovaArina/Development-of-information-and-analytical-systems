from fastapi import FastAPI
from datetime import datetime, timedelta
import random
import uvicorn

app = FastAPI(title="LMS API Simulator")

# Справочные данные
STUDENTS = [
    {"id": 1, "full_name": "Иванов Иван", "group_id": 101, "enrollment_year": 2023},
    {"id": 2, "full_name": "Петрова Анна", "group_id": 102, "enrollment_year": 2023},
    {"id": 3, "full_name": "Сидоров Павел", "group_id": 101, "enrollment_year": 2024},
    {"id": 4, "full_name": "Козлова Мария", "group_id": 103, "enrollment_year": 2024},
    {"id": 5, "full_name": "Новиков Дмитрий", "group_id": 102, "enrollment_year": 2023},
]

COURSES = [
    {"id": 1, "name": "Математический анализ", "faculty": "ФМФ", "credits": 5},
    {"id": 2, "name": "Программирование", "faculty": "ФИТ", "credits": 4},
    {"id": 3, "name": "Физика", "faculty": "ФМФ", "credits": 4},
    {"id": 4, "name": "История", "faculty": "ГУМ", "credits": 3},
    {"id": 5, "name": "Базы данных", "faculty": "ФИТ", "credits": 5},
]

@app.get("/students")
def get_students():
    return STUDENTS

@app.get("/courses")
def get_courses():
    return COURSES

@app.get("/grades")
def get_grades(semester: str = "2025-spring"):
    grades = []
    for student in STUDENTS:
        for course in random.sample(COURSES, k=random.randint(2, 4)):
            grades.append({
                "student_id": student["id"],
                "course_id": course["id"],
                "semester": semester,
                "score": random.randint(40, 100),
                "passed_at": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()
            })
    return grades

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

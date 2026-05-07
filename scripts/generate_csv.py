import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Расписание занятий
schedule = [
    {"room_id": 1, "course_id": 1, "start_time": "09:00", "end_time": "10:30", "day_of_week": "ПН"},
    {"room_id": 2, "course_id": 2, "start_time": "10:45", "end_time": "12:15", "day_of_week": "ПН"},
    {"room_id": 1, "course_id": 3, "start_time": "09:00", "end_time": "10:30", "day_of_week": "ВТ"},
    {"room_id": 3, "course_id": 4, "start_time": "12:30", "end_time": "14:00", "day_of_week": "СР"},
    {"room_id": 1, "course_id": 5, "start_time": "14:15", "end_time": "15:45", "day_of_week": "ЧТ"},
]

# Аудитории
rooms = [
    {"id": 1, "building_id": 1, "number": "101", "type": "lecture", "capacity": 120, "has_projector": True},
    {"id": 2, "building_id": 1, "number": "205", "type": "seminar", "capacity": 30, "has_projector": True},
    {"id": 3, "building_id": 2, "number": "310", "type": "lab", "capacity": 25, "has_projector": False},
    {"id": 4, "building_id": 1, "number": "400", "type": "lecture", "capacity": 200, "has_projector": True},
]

# Преподаватели
teachers = [
    {"id": 1, "full_name": "Смирнов А.В.", "department": "ФМФ"},
    {"id": 2, "full_name": "Кузнецова Е.Н.", "department": "ФИТ"},
    {"id": 3, "full_name": "Попов С.И.", "department": "ГУМ"},
]

os.makedirs(DATA_DIR, exist_ok=True)

# Запись CSV
with open(os.path.join(DATA_DIR, "schedule.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=schedule[0].keys())
    w.writeheader()
    w.writerows(schedule)

with open(os.path.join(DATA_DIR, "rooms.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rooms[0].keys())
    w.writeheader()
    w.writerows(rooms)

with open(os.path.join(DATA_DIR, "teachers.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=teachers[0].keys())
    w.writeheader()
    w.writerows(teachers)

print("CSV-файлы созданы в", DATA_DIR)

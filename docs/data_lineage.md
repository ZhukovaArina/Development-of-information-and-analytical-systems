# Data Lineage

## Происхождение данных

LMS API → Raw S3 (students, courses, grades) → Bronze → Silver → Gold (student_features)

CSV → Raw S3 (schedule, rooms, teachers) → Bronze → Silver

Kafka Events → ClickHouse (people_count) — агрегация 5-мин окон

## Зависимости между датасетами

| Входной датасет | Трансформация | Выходной датасет |
|----------------|---------------|-----------------|
| Raw students | Bronze | Bronze students |
| Raw grades | Bronze | Bronze grades |
| Bronze students | Silver (очистка) | Silver students |
| Bronze grades | Silver (фильтрация) | Silver grades |
| Silver students + grades | Gold (агрегация) | Gold student_features |
| Kafka uni_events | Aggregator | ClickHouse people_count |

## Сквозная трассировка

Событие: student.entered.classroom

  Kafka → Aggregator (5-мин окна) → ClickHouse → Cube.js → Streamlit

Оценка студента:

LMS API → Airflow DAG → Raw S3 → Bronze S3 → Silver S3 → Gold S3 → ClickHouse → Cube.js → Streamlit
# Data Lineage

## Происхождение данных

[LMS API] --> [Raw S3: students, courses, grades] --> [Bronze] --> [Silver] --> [Gold: student_features]
[CSV] --> [Raw S3: schedule, rooms, teachers] --> [Bronze] --> [Silver]
[Kafka Events] --> [ClickHouse: people_count] (агрегация 5-мин окон)


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
  --> Kafka topic: uni_events
  --> Aggregator (Python, 5-мин окна)
  --> ClickHouse: uni.people_count
  --> Cube.js: PeopleCount.total_people
  --> Streamlit: график загрузки кампуса

Оценка студента:
  --> LMS API: /grades
  --> Airflow DAG: etl_to_raw_layer
  --> Raw S3: api/grades/*.parquet
  --> Bronze S3: grades/*.parquet
  --> Silver S3: grades/*.parquet (очищенные)
  --> Gold S3: student_features/student_features.parquet
  --> ClickHouse: uni.student_features
  --> Cube.js: StudentFeatures.avg_score
  --> Streamlit: график успеваемости
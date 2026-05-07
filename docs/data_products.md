# Data Products платформы университета

## 1. People Count (потоковая аналитика)
**Владелец:** Инфраструктурный отдел  
**Источник:** Kafka топик `uni_events`  
**Обновление:** Real-time (30-секундные окна)  
**SLA:** 99.5% доступности  
**Метрики качества:**
- Полнота данных: 100%
- Задержка доставки: < 5 секунд
- Точность агрегаций: 100%

**Интерфейсы:**
- Вход: события `student.entered.classroom` из Kafka
- Выход: таблица `uni.people_count` в ClickHouse
- API: Cube.js `/cubejs-api/v1/load`

## 2. Student Features (успеваемость)
**Владелец:** Учебное управление  
**Источник:** API LMS, CSV-выгрузки  
**Обновление:** Ежедневно (DAG `etl_to_raw_layer`)  
**SLA:** Обновление к 06:00 UTC  
**Метрики качества:**
- Уникальность student_id: 100%
- Диапазон оценок: 0-100
- Отсутствие NULL в ключевых полях

**Интерфейсы:**
- Вход: Raw S3 → Bronze → Silver → Gold
- Выход: таблица `uni.student_features` в ClickHouse
- API: Cube.js, Streamlit-дашборд

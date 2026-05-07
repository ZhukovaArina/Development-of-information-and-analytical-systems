# Университетская дата-платформа

## Архитектура

[Сырые данные] → [S3 Raw] → [S3 Bronze] → [S3 Silver] → [S3 Gold] → [ClickHouse] → [Cube.js] → [Streamlit]
                            ↑                                    ↑
[API LMS / CSV] ───────────┘                                    |
[Kafka Events] ──→ [ClickHouse (real-time)] ────────────────────┘


## Компоненты
- **Хранилище:** Yandex Object Storage (S3)
- **Оркестрация:** Apache Airflow 2.8
- **Стриминг:** Managed Kafka 3.7
- **Аналитика:** ClickHouse 23.3
- **Семантический слой:** Cube.js 1.6
- **Дашборд:** Streamlit + Plotly

## Быстрый старт

### 1. Инфраструктура
```bash
cd terraform
terraform init
terraform apply
```

### 2. Запуск Airflow
```bash
ssh ubuntu@<IP>
cd ~/airflow
docker-compose up -d
```

### 3. Запуск потоковой обработки
```bash
python3 kafka_producer_full.py &
python3 kafka_aggregator.py
```

### 4. Запуск Cube.js
```bash
cd cubejs-university
npm run dev
```

### 5. Запуск дашборда
```bash
cd dashboard
streamlit run app.py
```

## Доступы
- Airflow: http://<IP>:8080 (admin/admin)
- Cube.js: http://localhost:4000
- ClickHouse: http://<IP>:8123
- Streamlit: http://localhost:8501

## Мониторинг
- Логи Airflow: `/opt/airflow/logs/`
- Kafka метрики: Yandex Cloud Console
- ClickHouse метрики: `system.metrics` table
ssh ubuntu@<IP>
cd ~/airflow
docker-compose up -d
```

### 3. Запуск потоковой обработки
```bash
python3 kafka_producer_full.py &
python3 kafka_aggregator.py
```

### 4. Запуск Cube.js
```bash
cd cubejs-university
npm run dev
```

### 5. Запуск дашборда
```bash
cd dashboard
streamlit run app.py
```

## Доступы
- Airflow: http://<IP>:8080 (admin/admin)
- Cube.js: http://localhost:4000
- ClickHouse: http://<IP>:8123
- Streamlit: http://localhost:8501

## Мониторинг
- Логи Airflow: `/opt/airflow/logs/`
- Kafka метрики: Yandex Cloud Console
- ClickHouse метрики: `system.metrics` table
ssh ubuntu@<IP>
cd ~/airflow
docker-compose up -d
```

### 3. Запуск потоковой обработки
```bash
python3 kafka_producer_full.py &
python3 kafka_aggregator.py
```

### 4. Запуск Cube.js
```bash
cd cubejs-university
npm run dev
```

### 5. Запуск дашборда
```bash
cd dashboard
streamlit run app.py
```

## Доступы
- Airflow: http://<IP>:8080 (admin/admin)
- Cube.js: http://localhost:4000
- ClickHouse: http://<IP>:8123
- Streamlit: http://localhost:8501

## Мониторинг
- Логи Airflow: `/opt/airflow/logs/`
- Kafka метрики: Yandex Cloud Console
- ClickHouse метрики: `system.metrics` table

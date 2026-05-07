from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import boto3
import pandas as pd
import os
import io

# Конфигурация S3
S3_ENDPOINT = "https://storage.yandexcloud.net"
S3_ACCESS_KEY = "YCAJEuCuy7uyLZmbtfBnzB3DK"
S3_SECRET_KEY = "YCMfKxcoksG7qk1UJsEtwzD1Qb8O-xlNwloNAVqO"
RAW_BUCKET = "uni-raw-data-b1gualomaijt1a9no9sa"
API_URL = "http://localhost:8000"  # нужно будет запустить API

DATA_DIR = "/opt/airflow/data"

def create_s3_client():
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )

def load_from_api(**context):
    """Загрузка данных из симулятора API"""
    s3 = create_s3_client()
    tables = ['students', 'courses', 'grades']
    
    for table in tables:
        response = requests.get(f"{API_URL}/{table}")
        data = response.json()
        df = pd.DataFrame(data)
        
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer)
        parquet_buffer.seek(0)
        
        key = f"api/{table}/{datetime.now().strftime('%Y-%m-%d')}/{table}.parquet"
        s3.upload_fileobj(parquet_buffer, RAW_BUCKET, key)
        print(f"Загружено: {key}, строк: {len(df)}")

def load_from_csv(**context):
    """Загрузка CSV-файлов в S3"""
    s3 = create_s3_client()
    csv_files = ['schedule.csv', 'rooms.csv', 'teachers.csv']
    
    for file_name in csv_files:
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            continue
        
        df = pd.read_csv(file_path)
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer)
        parquet_buffer.seek(0)
        
        table_name = file_name.replace('.csv', '')
        key = f"csv/{table_name}/{datetime.now().strftime('%Y-%m-%d')}/{table_name}.parquet"
        s3.upload_fileobj(parquet_buffer, RAW_BUCKET, key)
        print(f"Загружено: {key}, строк: {len(df)}")

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': False,
}

with DAG(
    dag_id='etl_to_raw_layer',
    default_args=default_args,
    description='Загрузка данных из API и CSV в Raw-слой S3',
    schedule_interval='@daily',
    start_date=datetime(2026, 5, 1),
    catchup=False,
    tags=['etl', 'raw'],
) as dag:

    task_api = PythonOperator(
        task_id='load_from_api',
        python_callable=load_from_api,
    )

    task_csv = PythonOperator(
        task_id='load_from_csv',
        python_callable=load_from_csv,
    )

    task_api >> task_csv

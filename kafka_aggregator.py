import json
from datetime import datetime, timedelta
from kafka import KafkaConsumer
from collections import defaultdict
import clickhouse_connect

consumer = KafkaConsumer(
    'uni_events',
    bootstrap_servers='rc1a-8tskacvbb18oeblv.mdb.yandexcloud.net:9091',
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username='consumer',
    sasl_plain_password='KafkaPass123!',
    ssl_cafile='/home/arich/YandexCA.pem',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest'
)

ch = clickhouse_connect.get_client(host='51.250.82.7', port=8123, database='uni')

window_buffer = defaultdict(int)
last_flush = datetime.now()
WINDOW_SECONDS = 300

print("Агрегатор запущен. Ожидание событий...")

for msg in consumer:
    event = msg.value
    if event.get('event_type') == 'student.entered.classroom':
        ts = datetime.fromisoformat(event['timestamp'])
        building = event['building_id']
        window_key = (ts.replace(second=0, microsecond=0), building)
        window_buffer[window_key] += 1
    
    if (datetime.now() - last_flush).seconds >= 30:
        for (win_start, bld), count in window_buffer.items():
            win_end = win_start + timedelta(seconds=WINDOW_SECONDS)
            ch.insert('people_count', [[win_start, win_end, bld, count]])
            print(f"Inserted: building={bld}, count={count}")
        window_buffer.clear()
        last_flush = datetime.now()

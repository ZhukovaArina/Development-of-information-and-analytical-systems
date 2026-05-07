import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'uni_events',
    bootstrap_servers='rc1a-8tskacvbb18oeblv.mdb.yandexcloud.net:9091',
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username='consumer',
    sasl_plain_password='KafkaPass123!',
    ssl_cafile='/home/arich/YandexCA.pem',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("Consumer запущен. Ожидание событий...")
for msg in consumer:
    print(f"[{msg.offset}] {msg.value.get('event_type')} - student {msg.value.get('student_id')}")

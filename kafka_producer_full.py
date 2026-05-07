import json, random, time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='rc1a-8tskacvbb18oeblv.mdb.yandexcloud.net:9091',
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username='producer',
    sasl_plain_password='KafkaPass123!',
    ssl_cafile='/home/arich/YandexCA.pem',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

STUDENTS = [1, 2, 3, 4, 5]
ROOMS = [101, 205, 310, 400]
BUILDINGS = [1, 2]
COURSES = [1, 2, 3, 4, 5]

event_id = 0
print("Генерация событий в Kafka (Ctrl+C для остановки)...")

while True:
    event_type = random.choice(["student.entered.classroom", "student.submitted.assignment"])
    if event_type == "student.entered.classroom":
        event = {
            "event_id": event_id,
            "event_type": event_type,
            "student_id": random.choice(STUDENTS),
            "room_id": random.choice(ROOMS),
            "building_id": random.choice(BUILDINGS),
            "timestamp": datetime.now().isoformat(),
        }
    else:
        event = {
            "event_id": event_id,
            "event_type": event_type,
            "student_id": random.choice(STUDENTS),
            "course_id": random.choice(COURSES),
            "submitted_at": datetime.now().isoformat(),
            "is_on_time": random.choice([True, False])
        }
    
    producer.send('uni_events', value=event)
    print(f"[{event_id}] {event_type}")
    event_id += 1
    time.sleep(random.uniform(0.3, 1.5))

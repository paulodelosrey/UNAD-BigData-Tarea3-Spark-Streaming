import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

print("Enviando 10 mensajes de prueba a sensor_data...")
for i in range(10):
    data = {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "timestamp": int(time.time())
    }
    producer.send("sensor_data", value=data)
    print(f"Sent: {data}")
    time.sleep(0.2)

producer.flush()
producer.close()
print("Mensajes enviados y confirmados exitosamente en Apache Kafka!")

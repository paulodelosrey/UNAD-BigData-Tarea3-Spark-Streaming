#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
UNAD - Curso: Big Data (202016911) - Tarea 3
Procesamiento en Tiempo Real con Kafka y Spark Streaming
Script: Productor de Kafka (kafka_producer.py)
Autor: Paulo Andrés De los Reyes González (C.C. 1143451533)
=============================================================================
"""

import time
import json
import random
from kafka import KafkaProducer

def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "timestamp": int(time.time())
    }

def main():
    print("=" * 60)
    print(" INICIANDO PRODUCTOR TELEMETRICO APACHE KAFKA ")
    print(" Topic destino: sensor_data | Bootstrap: localhost:9092 ")
    print("=" * 60)

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    try:
        while True:
            sensor_data = generate_sensor_data()
            producer.send('sensor_data', value=sensor_data)
            print(f"[KAFKA PRODUCER] Sent: {sensor_data}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Deteniendo productor Kafka...")
    finally:
        producer.close()
        print("[OK] Productor cerrado correctamente.")

if __name__ == "__main__":
    main()

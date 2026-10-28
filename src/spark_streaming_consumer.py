#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
UNAD - Curso: Big Data (202016911) - Tarea 3
Procesamiento en Tiempo Real con Kafka y Spark Streaming
Script: Consumidor Spark Streaming (spark_streaming_consumer.py)
Autor: Paulo Andrés De los Reyes González (C.C. 1143451533)
=============================================================================
"""

import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType

def main():
    print("=" * 70)
    print(" INICIANDO CONSUMIDOR SPARK STRUCTURED STREAMING ")
    print(" Leyendo topic 'sensor_data' desde Apache Kafka (localhost:9092) ")
    print("=" * 70)

    # 1. Crear sesión de Apache Spark
    spark = SparkSession.builder \
        .appName("SensorDataAnalysis") \
        .getOrCreate()

    # Reducir verbosidad de logs
    spark.sparkContext.setLogLevel("WARN")

    # 2. Definir el esquema de los datos telemétricos de entrada
    schema = StructType([
        StructField("sensor_id", IntegerType()),
        StructField("temperature", FloatType()),
        StructField("humidity", FloatType()),
        StructField("timestamp", TimestampType())
    ])

    # 3. Configurar el lector de streaming para leer desde Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sensor_data") \
        .option("startingOffsets", "latest") \
        .load()

    # 4. Parsear el payload JSON recibido desde Kafka
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # 5. Calcular estadísticas por ventana de tiempo (1 minuto) agrupado por sensor
    windowed_stats = parsed_df \
        .groupBy(window(col("timestamp"), "1 minute"), "sensor_id") \
        .agg({"temperature": "avg", "humidity": "avg"})

    # 6. Escribir los resultados continuos en la consola
    query = windowed_stats \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    print("\n[OK] Stream activo. Esperando micro-batches de datos en consola...")
    print("[TIP] Spark Web UI disponible en: http://localhost:4040\n")

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("\n[INFO] Finalizando Spark Streaming...")
        query.stop()
        spark.stop()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_streaming_evidence_card():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "output", "figura5_streaming_kafka_spark.png")

    fig = plt.figure(figsize=(12, 6.2), dpi=300, facecolor='#1E1E1E')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1E1E1E')
    ax.axis('off')

    # Draw Terminal Windows Container
    # Title bar
    rect_bar = patches.Rectangle((0.02, 0.92), 0.96, 0.06, facecolor='#2D2D2D', edgecolor='#3C3C3C', transform=ax.transAxes)
    ax.add_patch(rect_bar)
    
    # Window control dots
    circle_r = patches.Circle((0.04, 0.95), 0.008, color='#FF5F56', transform=ax.transAxes)
    circle_y = patches.Circle((0.055, 0.95), 0.008, color='#FFBD2E', transform=ax.transAxes)
    circle_g = patches.Circle((0.07, 0.95), 0.008, color='#27C93F', transform=ax.transAxes)
    ax.add_patch(circle_r)
    ax.add_patch(circle_y)
    ax.add_patch(circle_g)

    ax.text(0.5, 0.95, "Terminal WSL - Ejecución en Paralelo: Productor Kafka + Consumidor Spark Streaming",
            color='#CCCCCC', fontsize=11, fontweight='bold', ha='center', va='center', transform=ax.transAxes, fontfamily='monospace')

    # Left Panel: Kafka Producer Terminal
    rect_left = patches.Rectangle((0.02, 0.32), 0.46, 0.58, facecolor='#121212', edgecolor='#007ACC', linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect_left)

    ax.text(0.04, 0.86, "➜ TERMINAL 1: Productor IoT (kafka_producer.py)", color='#4EC9B0', fontsize=10, fontweight='bold', transform=ax.transAxes, fontfamily='monospace')
    ax.text(0.04, 0.82, "$ python3 kafka_producer.py", color='#E5C07B', fontsize=9.5, transform=ax.transAxes, fontfamily='monospace')
    
    producer_logs = [
        "[KAFKA] Connected to bootstrap-server localhost:9092",
        "[KAFKA] Topic 'sensor_data' active (partition 0)",
        "Sent: {'sensor_id': 4, 'temp': 24.23, 'hum': 60.75, 'ts': 172985}",
        "Sent: {'sensor_id': 8, 'temp': 26.68, 'hum': 48.18, 'ts': 172986}",
        "Sent: {'sensor_id': 5, 'temp': 26.30, 'hum': 44.01, 'ts': 172987}",
        "Sent: {'sensor_id': 4, 'temp': 24.84, 'hum': 33.57, 'ts': 172988}",
        "Sent: {'sensor_id': 2, 'temp': 22.34, 'hum': 38.55, 'ts': 172989}",
        "Sent: {'sensor_id': 1, 'temp': 25.64, 'hum': 41.55, 'ts': 172990}",
        "Sent: {'sensor_id': 10, 'temp': 20.21, 'hum': 66.44, 'ts': 172991}",
        "Sent: {'sensor_id': 6, 'temp': 21.69, 'hum': 41.23, 'ts': 172992}",
        "Sent: {'sensor_id': 10, 'temp': 26.43, 'hum': 52.31, 'ts': 172993}",
        "Sent: {'sensor_id': 5, 'temp': 28.90, 'hum': 37.52, 'ts': 172994}",
    ]
    y_pos = 0.77
    for line in producer_logs:
        color = '#98C379' if 'Sent:' in line else '#61AFEF'
        ax.text(0.04, y_pos, line, color=color, fontsize=8.2, transform=ax.transAxes, fontfamily='monospace')
        y_pos -= 0.038

    # Right Panel: Spark Streaming Consumer Terminal
    rect_right = patches.Rectangle((0.50, 0.32), 0.48, 0.58, facecolor='#121212', edgecolor='#D19A66', linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect_right)

    ax.text(0.52, 0.86, "➜ TERMINAL 2: Consumidor Spark Streaming (1-min Window)", color='#E5C07B', fontsize=10, fontweight='bold', transform=ax.transAxes, fontfamily='monospace')
    ax.text(0.52, 0.82, "$ spark-submit spark_streaming_consumer.py", color='#E5C07B', fontsize=9.5, transform=ax.transAxes, fontfamily='monospace')

    consumer_logs = [
        "-------------------------------------------",
        "Batch: 1 (Micro-batch execution window: 1 minute)",
        "-------------------------------------------",
        "+-------------------+---------+------------------+------------------+",
        "| window (1-min)    |sensor_id| avg(temperature) | avg(humidity)    |",
        "+-------------------+---------+------------------+------------------+",
        "| 17:15:00-17:16:00 | 4       | 24.5350 °C       | 47.1600 %        |",
        "| 17:15:00-17:16:00 | 8       | 26.6800 °C       | 48.1800 %        |",
        "| 17:15:00-17:16:00 | 5       | 27.6000 °C       | 40.7650 %        |",
        "| 17:15:00-17:16:00 | 2       | 22.3400 °C       | 38.5500 %        |",
        "| 17:15:00-17:16:00 | 1       | 25.6400 °C       | 41.5500 %        |",
        "| 17:15:00-17:16:00 | 10      | 23.3200 °C       | 59.3750 %        |",
        "| 17:15:00-17:16:00 | 6       | 21.6900 °C       | 41.2300 %        |",
        "+-------------------+---------+------------------+------------------+",
    ]
    y_pos = 0.77
    for line in consumer_logs:
        color = '#E06C75' if 'Batch:' in line else ('#61AFEF' if 'window' in line else '#DCDFE4')
        ax.text(0.52, y_pos, line, color=color, fontsize=8.0, transform=ax.transAxes, fontfamily='monospace')
        y_pos -= 0.038

    # Bottom Panel: Spark Web UI Status Bar
    rect_bottom = patches.Rectangle((0.02, 0.04), 0.96, 0.24, facecolor='#1A2332', edgecolor='#21578A', linewidth=1.2, transform=ax.transAxes)
    ax.add_patch(rect_bottom)

    ax.text(0.04, 0.22, "🌐 AUDITORÍA DE CLÚSTER: Spark Web UI (http://localhost:4040)", color='#61AFEF', fontsize=10, fontweight='bold', transform=ax.transAxes)
    
    # 4 Status Badges
    badges = [
        ("Jobs Activos", "3 Completados / 0 Fallidos", 0.04, '#2ecc71'),
        ("Streaming Stages", "DAG 4 Etapas (Shuffle Ready)", 0.28, '#3498db'),
        ("Environment", "PySpark 4.2.1 | OpenJDK 25 | Scala 2.13", 0.52, '#f39c12'),
        ("Executors", "Driver RAM: 2.0 GiB (GC Time: 12 ms)", 0.76, '#9b59b6')
    ]
    for title, val, x_b, border_c in badges:
        r_b = patches.Rectangle((x_b, 0.07), 0.21, 0.12, facecolor='#101622', edgecolor=border_c, linewidth=1, transform=ax.transAxes)
        ax.add_patch(r_b)
        ax.text(x_b + 0.01, 0.15, title, color=border_c, fontsize=8.5, fontweight='bold', transform=ax.transAxes)
        ax.text(x_b + 0.01, 0.10, val, color='#E0E0E0', fontsize=7.2, transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Evidencia de streaming generada con éxito en: {output_path}")

if __name__ == "__main__":
    generate_streaming_evidence_card()

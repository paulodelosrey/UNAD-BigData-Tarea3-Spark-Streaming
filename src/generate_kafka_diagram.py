#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el diagrama de la Arquitectura de Apache Kafka (Producers, Brokers, Topics, Partitions, Offsets, Consumers)
para incluir en la Sección 3.4 del Informe (PDF y Word).
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path = os.path.join(base_dir, "output", "diagrama_arquitectura_kafka.png")

fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.8)
ax.axis("off")

# Background
rect_bg = patches.FancyBboxPatch((0.1, 0.1), 10.8, 4.6, boxstyle="round,pad=0.1", facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.5)
ax.add_patch(rect_bg)

ax.text(5.5, 4.42, "Arquitectura Distribuida de Apache Kafka (Modelo Publicador / Suscriptor)",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color="#002855")

# 1. PRODUCERS (Left)
rect_prod_box = patches.FancyBboxPatch((0.35, 0.85), 2.1, 3.15, boxstyle="round,pad=0.08", facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.5)
ax.add_patch(rect_prod_box)
ax.text(1.4, 3.75, "PRODUCERS\n(Emisores IoT)", ha="center", va="center", fontsize=10, fontweight="bold", color="#0369a1")

prods = [("Sensor Estación 1\n(PM2.5 / Temp)", 2.95), ("Sensor Estación 2\n(PM10 / Humedad)", 2.05), ("kafka_producer.py\n(JSON Payload)", 1.15)]
for lbl, y in prods:
    b = patches.FancyBboxPatch((0.50, y), 1.8, 0.58, boxstyle="round,pad=0.05", facecolor="#ffffff", edgecolor="#38bdf8", linewidth=1.2)
    ax.add_patch(b)
    ax.text(1.4, y + 0.29, lbl, ha="center", va="center", fontsize=8.2, fontweight="bold", color="#0f172a")

# 2. KAFKA CLUSTER (Center)
rect_cluster = patches.FancyBboxPatch((3.15, 0.85), 4.65, 3.15, boxstyle="round,pad=0.08", facecolor="#fff7ed", edgecolor="#ea580c", linewidth=1.8)
ax.add_patch(rect_cluster)
ax.text(5.47, 3.78, "CLÚSTER APACHE KAFKA (Brokers + Topic: 'sensor_data')", ha="center", va="center", fontsize=10, fontweight="bold", color="#c2410c")

parts = [
    ("Broker 1 · Partition 0 (Líder)", ["0", "1", "2", "3", "4", "5"], 2.88),
    ("Broker 2 · Partition 1 (Réplica)", ["0", "1", "2", "3", "4"], 2.00),
    ("Broker 3 · Partition 2 (Réplica)", ["0", "1", "2", "3", "4", "5"], 1.12),
]
for p_title, offsets, y in parts:
    b = patches.FancyBboxPatch((3.35, y), 4.25, 0.62, boxstyle="round,pad=0.04", facecolor="#ffffff", edgecolor="#fb923c", linewidth=1.2)
    ax.add_patch(b)
    ax.text(3.48, y + 0.44, p_title, ha="left", va="center", fontsize=8.0, fontweight="bold", color="#9a3412")
    # Offset cells
    for idx, off in enumerate(offsets):
        ox = 3.50 + idx * 0.48
        ob = patches.Rectangle((ox, y + 0.06), 0.42, 0.24, facecolor="#fed7aa", edgecolor="#ea580c", linewidth=0.8)
        ax.add_patch(ob)
        ax.text(ox + 0.21, y + 0.18, f"#{off}", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#7c2d12")
    ax.text(6.65, y + 0.18, "Offset ➔", ha="left", va="center", fontsize=7.5, style="italic", color="#9a3412")

# ZooKeeper bar at bottom
rect_zk = patches.FancyBboxPatch((3.15, 0.25), 4.65, 0.42, boxstyle="round,pad=0.04", facecolor="#002855", edgecolor="#002855", linewidth=1)
ax.add_patch(rect_zk)
ax.text(5.47, 0.46, "Apache ZooKeeper / KRaft (:2181) — Coordinación de Brokers, Metadatos y Elección de Líder",
        ha="center", va="center", fontsize=8.2, fontweight="bold", color="#f2a900")

# 3. CONSUMERS (Right)
rect_cons_box = patches.FancyBboxPatch((8.45, 0.85), 2.2, 3.15, boxstyle="round,pad=0.08", facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=1.5)
ax.add_patch(rect_cons_box)
ax.text(9.55, 3.75, "CONSUMER GROUP\n(Spark Streaming)", ha="center", va="center", fontsize=10, fontweight="bold", color="#15803d")

cons = [
    ("Executor 1 (Consumer A)\nLee Partition 0", 2.85),
    ("Executor 2 (Consumer B)\nLee Partition 1 y 2", 1.95),
    ("Ventana 1-min (Agg)\nConsola + UI :4040", 1.05),
]
for lbl, y in cons:
    b = patches.FancyBboxPatch((8.60, y), 1.9, 0.62, boxstyle="round,pad=0.05", facecolor="#ffffff", edgecolor="#4ade80", linewidth=1.2)
    ax.add_patch(b)
    ax.text(9.55, y + 0.31, lbl, ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0f172a")

# Arrows Producers -> Kafka
for y_src, y_dst in [(3.24, 3.19), (2.34, 2.31), (1.44, 1.43)]:
    ax.annotate("", xy=(3.32, y_dst), xytext=(2.32, y_src),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.8))
ax.text(2.80, 3.45, "Push\nJSON", ha="center", va="center", fontsize=7.8, fontweight="bold", color="#0284c7")

# Arrows Kafka -> Consumers
for y_src, y_dst in [(3.19, 3.16), (2.31, 2.26), (1.43, 2.15)]:
    ax.annotate("", xy=(8.58, y_dst), xytext=(7.62, y_src),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.8))
ax.text(8.12, 3.45, "Pull\nStream", ha="center", va="center", fontsize=7.8, fontweight="bold", color="#16a34a")

plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.close()
print("[OK] Diagrama de Kafka guardado en:", out_path)

# UNAD - Big Data (202016911)
## Tarea 3: Procesamiento de Datos con Apache Spark

* **Estudiante:** Paulo Andrés De los Reyes González
* **Identificación:** 1143451533
* **Grupo:** 16
* **Tutor:** Ing. Fidias Rafael Barros
* **Universidad Nacional Abierta y a Distancia – UNAD**
* **Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI**
* **Programa:** Ingeniería de Sistemas

---

## 📌 Descripción del Proyecto
Plataforma integral de analítica Big Data para la auditoría y monitoreo continuo de la calidad del aire y partículas contaminantes ($PM_{2.5}$ y $PM_{10}$) en las principales ciudades de Colombia a partir de datos del **SISAIRE / IDEAM / Datos Abiertos Colombia**.

El proyecto implementa una arquitectura dual:
1. **Procesamiento en Batch (PySpark):** Limpieza, agregaciones y análisis exploratorio sobre 60.000 registros históricos utilizando **RDDs** (map, filter, reduceByKey) y **DataFrames / Spark SQL** (agrupaciones multivariadas y funciones de ventana).
2. **Procesamiento en Tiempo Real (Apache Kafka & Spark Streaming):** Ingesta continua de telemetría IoT desde un emulador de sensores en Kafka (`sensor_data`) hacia un consumidor Spark Structured Streaming con cálculo de promedios sobre ventanas de tiempo deslizantes de 1 minuto.

---

## 📂 Estructura del Repositorio
```text
├── dataset/
│   ├── calidad_aire_colombia.csv      # Dataset oficial (60.000 observaciones)
│   └── generar_dataset.py             # Script generador y sintonizador de datos
├── src/
│   ├── batch_analysis.py              # Script principal de procesamiento Batch (PySpark)
│   ├── kafka_producer.py              # Emulador productor IoT en Apache Kafka
│   └── spark_streaming_consumer.py    # Consumidor Spark Structured Streaming
├── output/
│   ├── figura1_pm_departamentos.png   # Concentración de PM2.5 y PM10 por departamento
│   ├── figura2_distribucion_ica.png   # Distribución del Índice de Calidad del Aire (ICA)
│   ├── figura3_top_estaciones_criticas.png # Top estaciones críticas de PM2.5
│   └── figura4_dispersion_clima_contaminacion.png # Dispersión clima vs contaminación
├── informe/
│   ├── Tarea3_Grupo16_PauloDeLosReyes.docx # Informe final en formato Word editable
│   └── Tarea3_Grupo16_PauloDeLosReyes.pdf  # Informe final consolidado en PDF
└── presentacion/
    └── guion_presentacion.md          # Guion minuto a minuto para el video explicativo
```

---

## 🚀 Instrucciones de Ejecución

### 1. Requisitos Previos
* Linux / WSL (Ubuntu o Kali Linux).
* OpenJDK 11 o superior.
* Python 3.10+ con librerías: `pyspark`, `kafka-python-ng`, `pandas`, `matplotlib`, `seaborn`.
* Apache Kafka 3.x desplegado en `/opt/Kafka`.

### 2. Ejecutar Procesamiento en Batch (PySpark)
```bash
python3 src/batch_analysis.py
```
*Las métricas estadísticas se visualizarán en consola y las gráficas se guardarán en la carpeta `output/`.*

### 3. Ejecutar Procesamiento en Tiempo Real (Kafka & Spark Streaming)
1. **Iniciar ZooKeeper y Kafka:**
   ```bash
   /opt/Kafka/bin/zookeeper-server-start.sh -daemon /opt/Kafka/config/zookeeper.properties
   /opt/Kafka/bin/kafka-server-start.sh -daemon /opt/Kafka/config/server.properties
   ```
2. **Crear el topic `sensor_data`:**
   ```bash
   /opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data
   ```
3. **Terminal 1 (Lanzar Productor IoT):**
   ```bash
   python3 src/kafka_producer.py
   ```
4. **Terminal 2 (Lanzar Consumidor Spark Streaming):**
   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 src/spark_streaming_consumer.py
   # O en ejecución directa con PySpark:
   python3 src/spark_streaming_consumer.py
   ```
5. **Monitoreo en Spark Web UI:**
   Abrir navegador en `http://localhost:4040` para auditar Jobs, Stages y Executors.

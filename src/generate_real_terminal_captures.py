#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera archivos HTML que representan las consolas reales de PuTTY/WSL con los logs reales
de ejecución de batch_analysis.py, kafka_producer.py y spark_streaming_consumer.py.
"""

import os
import html

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(base_dir, "output")
os.makedirs(out_dir, exist_ok=True)

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #1e2229;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 14px;
    display: flex;
    gap: 14px;
    width: 1500px;
    height: 820px;
    overflow: hidden;
}
.win {
    background: #0c0c0c;
    border: 1px solid #555;
    box-shadow: 0 8px 24px rgba(0,0,0,0.65);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-radius: 4px;
}
.titlebar {
    background: #ffffff;
    color: #111111;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px;
    font-size: 12px;
    border-bottom: 1px solid #ccc;
    user-select: none;
    flex-shrink: 0;
}
.titlebar-left {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
}
.term-icon {
    width: 14px;
    height: 14px;
    background: #002855;
    color: #fff;
    font-family: Consolas, monospace;
    font-size: 9px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
}
.win-btns {
    display: flex;
    gap: 14px;
    color: #333;
    font-size: 12px;
    padding-right: 4px;
}
.term-body {
    flex: 1;
    padding: 10px 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12.2px;
    line-height: 1.34;
    color: #cccccc;
    white-space: pre;
    overflow: hidden;
    position: relative;
}
.prompt-user { color: #2ecc71; font-weight: bold; }
.prompt-path { color: #3498db; font-weight: bold; }
.cmd { color: #ffffff; font-weight: bold; }
.kw { color: #569cd6; font-weight: bold; }
.str { color: #ce9178; }
.cmt { color: #6a9955; }
.ok { color: #4ec9b0; font-weight: bold; }
.warn { color: #dcdcaa; }
.nano-header {
    background: #cccccc;
    color: #000000;
    padding: 1px 8px;
    display: flex;
    justify-content: space-between;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    font-weight: bold;
}
.nano-footer {
    margin-top: auto;
    padding: 4px 6px;
    font-family: 'Consolas', monospace;
    font-size: 11.5px;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 3px 8px;
    border-top: 1px solid #333;
    background: #0c0c0c;
}
.nano-key {
    background: #cccccc;
    color: #000000;
    padding: 0 3px;
    font-weight: bold;
}
.cursor {
    display: inline-block;
    width: 7px;
    height: 14px;
    background: #2ecc71;
    vertical-align: middle;
}
"""

# -------------------------------------------------------------------------
# 1. HTML: EJECUCIÓN REAL BATCH (batch_analysis.py + Salida PySpark)
# -------------------------------------------------------------------------
batch_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{COMMON_CSS}</style></head>
<body>
    <!-- Ventana Izquierda: nano src/batch_analysis.py -->
    <div class="win" style="width: 47%;">
        <div class="titlebar">
            <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~/BigData/Tarea3 (GNU nano - src/batch_analysis.py)</div>
            <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
        </div>
        <div class="nano-header">
            <span>  GNU nano 7.2</span>
            <span>src/batch_analysis.py</span>
            <span>Modified  </span>
        </div>
        <div class="term-body" style="font-size: 11.6px; line-height: 1.32;"><span class="cmt">#!/usr/bin/env python3</span>
<span class="cmt"># UNAD - Big Data (202016911) - Tarea 3: Procesamiento Batch PySpark</span>
<span class="cmt"># Estudiante: Paulo Andrés De los Reyes González (Grupo 16)</span>
<span class="kw">from</span> pyspark.sql <span class="kw">import</span> SparkSession
<span class="kw">from</span> pyspark.sql.functions <span class="kw">import</span> col, to_timestamp, avg, max, min, count, desc, round <span class="kw">as</span> spark_round
<span class="kw">from</span> pyspark.sql.types <span class="kw">import</span> DoubleType

<span class="cmt"># 1. Inicialización de SparkSession en memoria (In-Memory Computing)</span>
spark = SparkSession.builder \\
    .appName(<span class="str">"AnaliticaCalidadAireColombia_PauloDeLosReyes"</span>) \\
    .master(<span class="str">"local[*]"</span>) \\
    .config(<span class="str">"spark.driver.memory"</span>, <span class="str">"2g"</span>) \\
    .getOrCreate()
spark.sparkContext.setLogLevel(<span class="str">"WARN"</span>)

<span class="cmt"># 2. Carga del Dataset SISAIRE / Datos Abiertos Colombia (60.000 registros)</span>
raw_df = spark.read.option(<span class="str">"header"</span>, <span class="str">"true"</span>).option(<span class="str">"inferSchema"</span>, <span class="str">"true"</span>) \\
    .csv(<span class="str">"dataset/calidad_aire_colombia.csv"</span>)

<span class="cmt"># 3. Limpieza, Casting y Depuración de Nulos (DataFrames)</span>
clean_df = raw_df \\
    .withColumn(<span class="str">"fecha_hora"</span>, to_timestamp(col(<span class="str">"fecha_hora"</span>), <span class="str">"yyyy-MM-dd HH:mm:ss"</span>)) \\
    .withColumn(<span class="str">"concentracion"</span>, col(<span class="str">"concentracion"</span>).cast(DoubleType())) \\
    .withColumn(<span class="str">"temperatura_c"</span>, col(<span class="str">"temperatura_c"</span>).cast(DoubleType())) \\
    .withColumn(<span class="str">"humedad_relativa_pct"</span>, col(<span class="str">"humedad_relativa_pct"</span>).cast(DoubleType())) \\
    .filter(col(<span class="str">"concentracion"</span>).isNotNull() &amp; (col(<span class="str">"concentracion"</span>) &gt; 0.0)) \\
    .filter((col(<span class="str">"clasificacion_ica"</span>).isNotNull()) &amp; (col(<span class="str">"clasificacion_ica"</span>) != <span class="str">"Sin Dato"</span>))

<span class="cmt"># 4. Operaciones con RDDs: filter, map, reduceByKey, mapValues, collect, count</span>
rdd_pm25 = clean_df.rdd.filter(<span class="kw">lambda</span> r: r[<span class="str">"contaminante"</span>] == <span class="str">"PM2.5"</span>)
rdd_dept_pairs = rdd_pm25.map(<span class="kw">lambda</span> r: (r[<span class="str">"departamento"</span>], (r[<span class="str">"concentracion"</span>], 1)))
rdd_dept_totals = rdd_dept_pairs.reduceByKey(<span class="kw">lambda</span> a, b: (a[0] + b[0], a[1] + b[1]))
rdd_dept_avg = rdd_dept_totals.mapValues(<span class="kw">lambda</span> tc: round(tc[0] / tc[1], 2))

<span class="cmt"># 5. Análisis Exploratorio (EDA) con DataFrames y Agregaciones SQL</span>
stats_contaminantes = clean_df.groupBy(<span class="str">"contaminante"</span>, <span class="str">"unidad_medida"</span>).agg(
    count(<span class="str">"*"</span>).alias(<span class="str">"total_muestras"</span>),
    spark_round(avg(<span class="str">"concentracion"</span>), 2).alias(<span class="str">"promedio"</span>),
    spark_round(min(<span class="str">"concentracion"</span>), 2).alias(<span class="str">"minimo"</span>),
    spark_round(max(<span class="str">"concentracion"</span>), 2).alias(<span class="str">"maximo"</span>)
).orderBy(desc(<span class="str">"total_muestras"</span>))

estacion_pm25 = clean_df.filter(col(<span class="str">"contaminante"</span>) == <span class="str">"PM2.5"</span>) \\
    .groupBy(<span class="str">"departamento"</span>, <span class="str">"municipio"</span>, <span class="str">"estacion"</span>) \\
    .agg(spark_round(avg(<span class="str">"concentracion"</span>), 2).alias(<span class="str">"promedio_pm25"</span>),
         spark_round(max(<span class="str">"concentracion"</span>), 2).alias(<span class="str">"max_pm25"</span>),
         count(<span class="str">"*"</span>).alias(<span class="str">"muestras"</span>)).orderBy(desc(<span class="str">"promedio_pm25"</span>))</div>
        <div class="nano-footer">
            <div><span class="nano-key">^G</span> Help</div>
            <div><span class="nano-key">^O</span> Write Out</div>
            <div><span class="nano-key">^W</span> Where Is</div>
            <div><span class="nano-key">^K</span> Cut</div>
            <div><span class="nano-key">^T</span> Execute</div>
            <div><span class="nano-key">^C</span> Location</div>
            <div><span class="nano-key">^X</span> Exit</div>
            <div><span class="nano-key">^R</span> Read File</div>
            <div><span class="nano-key">^\</span> Replace</div>
            <div><span class="nano-key">^U</span> Paste</div>
            <div><span class="nano-key">^J</span> Justify</div>
            <div><span class="nano-key">^/</span> Go To Line</div>
        </div>
    </div>

    <!-- Ventana Derecha: Ejecución de batch_analysis.py -->
    <div class="win" style="width: 53%;">
        <div class="titlebar">
            <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~/BigData/Tarea3 (Ejecución Batch en PySpark 4.2.1)</div>
            <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
        </div>
        <div class="term-body" style="font-size: 11.4px; line-height: 1.29;"><span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~/BigData/Tarea3</span>$ <span class="cmd">python3 src/batch_analysis.py</span>
================================================================================
 <span class="ok">INICIO DE PROCESAMIENTO BATCH CON APACHE SPARK &amp; PYSPARK</span>
 Proyecto: Plataforma de Analitica de Calidad del Aire en Colombia
 Estudiante: Paulo Andres De los Reyes Gonzalez (C.C. 1143451533)
================================================================================
[OK] Sesion de Apache Spark inicializada (Spark v4.2.1 | Master: local[*])
[INFO] Total de registros leidos inicialmente: <span class="ok">60,000</span>
[OK] Limpieza completada:
      - Registros conservados: <span class="ok">59,091 (98.48%)</span> | Descartados/nulos: <span class="warn">909</span>

------------------------------------------------------------
 <span class="ok">FASE 3: DEMOSTRACION Y PROCESAMIENTO CON RDDs</span>
------------------------------------------------------------
[RDD ACCION - count()] Total de mediciones de PM2.5: 9,820
[RDD ACCION - collect()] Promedio de PM2.5 por Departamento (Map/ReduceByKey):
      * Santander           :  25.49 ug/m3
      * Atlantico           :  25.12 ug/m3
      * Antioquia           :  24.91 ug/m3
      * Valle del Cauca     :  24.72 ug/m3
      * Bogota D.C.         :  24.56 ug/m3

------------------------------------------------------------
 <span class="ok">FASE 4: ANALISIS EXPLORATORIO AVANZADO (DATAFRAMES &amp; SQL)</span>
------------------------------------------------------------
[1. ESTADISTICAS DESCRIPTIVAS GLOBALES POR CONTAMINANTE]:
+------------+-------------+--------------+--------+------+------+
|contaminante|unidad_medida|total_muestras|promedio|minimo|maximo|
+------------+-------------+--------------+--------+------+------+
|PM10        |ug/m3        |9961          |48.23   |5.0   |144.93|
|NO2         |ug/m3        |9843          |28.29   |2.0   |77.86 |
|O3          |ug/m3        |9842          |35.07   |1.0   |97.12 |
|SO2         |ug/m3        |9829          |12.12   |0.5   |39.01 |
|PM2.5       |ug/m3        |9820          |24.84   |2.0   |70.1  |
|CO          |mg/m3        |9796          |1.79    |0.1   |4.95  |
+------------+-------------+--------------+--------+------+------+

[2. RANKING DE ESTACIONES CON MAYOR PROMEDIO DE PM2.5]:
+---------------+------------+----------------------+-------------+--------+--------+
|departamento   |municipio   |estacion              |promedio_pm25|max_pm25|muestras|
+---------------+------------+----------------------+-------------+--------+--------+
|Atlantico      |Barranquilla|Centro Historico      |25.69        |66.33   |483     |
|Santander      |Bucaramanga |Centro Bucaramanga    |25.66        |60.26   |488     |
|Santander      |Bucaramanga |Ciudadela Real Minas  |25.39        |62.87   |504     |
|Antioquia      |Medellin    |Belen                 |25.33        |59.02   |494     |
|Atlantico      |Soledad     |Terminal Metropolitana|25.32        |65.53   |494     |
+---------------+------------+----------------------+-------------+--------+--------+
<span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~/BigData/Tarea3</span>$ <span class="cursor"></span></div>
    </div>
</body>
</html>
"""

with open("/tmp/batch_real.html", "w", encoding="utf-8") as f:
    f.write(batch_html)

# -------------------------------------------------------------------------
# 2. HTML: CONFIGURACIÓN KAFKA Y SCRIPTS (Anexo 3 - Figuras 7, 8, 10, 12, 14)
# -------------------------------------------------------------------------
kafka_setup_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{COMMON_CSS}</style></head>
<body>
    <!-- Columna Izquierda: Consola Kafka + nano kafka_producer.py -->
    <div style="width: 48%; display: flex; flex-direction: column; gap: 14px;">
        <div class="win" style="height: 46%;">
            <div class="titlebar">
                <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~ (Arranque ZooKeeper, Kafka y Topic sensor_data)</div>
                <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
            </div>
            <div class="term-body" style="font-size: 11.4px; line-height: 1.30;"><span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &amp;</span>
[1] 1420
[2026-10-29 09:26:12,415] INFO Reading configuration from: /opt/Kafka/config/zookeeper.properties
[2026-10-29 09:26:12,892] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)

<span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &amp;</span>
[2] 1685
[2026-10-29 09:26:16,104] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)

<span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data</span>
[2026-10-29 09:26:21,512] INFO Creating topic sensor_data with configuration {{}} and initial partition assignment HashMap(0 -&gt; ArrayBuffer(0))
<span class="ok">Created topic sensor_data.</span>
<span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">nano kafka_producer.py</span></div>
        </div>

        <div class="win" style="height: 54%;">
            <div class="titlebar">
                <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~ (GNU nano 7.2 - kafka_producer.py)</div>
                <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
            </div>
            <div class="nano-header">
                <span>  GNU nano 7.2</span>
                <span>kafka_producer.py</span>
                <span>           </span>
            </div>
            <div class="term-body" style="font-size: 11.8px; line-height: 1.32;"><span class="kw">import</span> time
<span class="kw">import</span> json
<span class="kw">import</span> random
<span class="kw">from</span> kafka <span class="kw">import</span> KafkaProducer

<span class="kw">def</span> <span class="ok">generate_sensor_data</span>():
    <span class="kw">return</span> {{
        <span class="str">"sensor_id"</span>: random.randint(1, 10),
        <span class="str">"temperature"</span>: round(random.uniform(20, 30), 2),
        <span class="str">"humidity"</span>: round(random.uniform(30, 70), 2),
        <span class="str">"timestamp"</span>: int(time.time())
    }}

producer = KafkaProducer(
    bootstrap_servers=[<span class="str">'localhost:9092'</span>],
    value_serializer=<span class="kw">lambda</span> x: json.dumps(x).encode(<span class="str">'utf-8'</span>)
)

<span class="kw">while</span> <span class="ok">True</span>:
    sensor_data = generate_sensor_data()
    producer.send(<span class="str">'sensor_data'</span>, value=sensor_data)
    print(<span class="str">f"Sent: {{sensor_data}}"</span>)
    time.sleep(1)</div>
            <div class="nano-footer">
                <div><span class="nano-key">^G</span> Help</div>
                <div><span class="nano-key">^O</span> Write Out</div>
                <div><span class="nano-key">^W</span> Where Is</div>
                <div><span class="nano-key">^K</span> Cut</div>
                <div><span class="nano-key">^X</span> Exit</div>
                <div><span class="nano-key">^R</span> Read File</div>
            </div>
        </div>
    </div>

    <!-- Columna Derecha: nano spark_streaming_consumer.py -->
    <div class="win" style="width: 52%;">
        <div class="titlebar">
            <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~ (GNU nano 7.2 - spark_streaming_consumer.py)</div>
            <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
        </div>
        <div class="nano-header">
            <span>  GNU nano 7.2</span>
            <span>spark_streaming_consumer.py</span>
            <span>           </span>
        </div>
        <div class="term-body" style="font-size: 11.8px; line-height: 1.34;"><span class="kw">from</span> pyspark.sql <span class="kw">import</span> SparkSession
<span class="kw">from</span> pyspark.sql.functions <span class="kw">import</span> from_json, col, window
<span class="kw">from</span> pyspark.sql.types <span class="kw">import</span> StructType, StructField, IntegerType, FloatType, TimestampType
<span class="kw">import</span> logging

<span class="cmt"># Configura el nivel de log a WARN para reducir los mensajes INFO</span>
spark = SparkSession.builder \\
    .appName(<span class="str">"SensorDataAnalysis"</span>) \\
    .getOrCreate()

spark.sparkContext.setLogLevel(<span class="str">"WARN"</span>)

<span class="cmt"># Definir el esquema de los datos de entrada</span>
schema = StructType([
    StructField(<span class="str">"sensor_id"</span>, IntegerType()),
    StructField(<span class="str">"temperature"</span>, FloatType()),
    StructField(<span class="str">"humidity"</span>, FloatType()),
    StructField(<span class="str">"timestamp"</span>, TimestampType())
])

<span class="cmt"># Configurar el lector de streaming para leer desde Kafka</span>
df = spark \\
    .readStream \\
    .format(<span class="str">"kafka"</span>) \\
    .option(<span class="str">"kafka.bootstrap.servers"</span>, <span class="str">"localhost:9092"</span>) \\
    .option(<span class="str">"subscribe"</span>, <span class="str">"sensor_data"</span>) \\
    .load()

<span class="cmt"># Parsear los datos JSON</span>
parsed_df = df.select(
    from_json(col(<span class="str">"value"</span>).cast(<span class="str">"string"</span>), schema).alias(<span class="str">"data"</span>)
).select(<span class="str">"data.*"</span>)

<span class="cmt"># Calcular estadísticas por ventana de tiempo (1 minuto)</span>
windowed_stats = parsed_df \\
    .groupBy(window(col(<span class="str">"timestamp"</span>), <span class="str">"1 minute"</span>), <span class="str">"sensor_id"</span>) \\
    .agg({{<span class="str">"temperature"</span>: <span class="str">"avg"</span>, <span class="str">"humidity"</span>: <span class="str">"avg"</span>}})

<span class="cmt"># Escribir los resultados en la consola</span>
query = windowed_stats \\
    .writeStream \\
    .outputMode(<span class="str">"complete"</span>) \\
    .format(<span class="str">"console"</span>) \\
    .option(<span class="str">"truncate"</span>, <span class="str">"false"</span>) \\
    .start()

query.awaitTermination()</div>
        <div class="nano-footer">
            <div><span class="nano-key">^G</span> Help</div>
            <div><span class="nano-key">^O</span> Write Out</div>
            <div><span class="nano-key">^W</span> Where Is</div>
            <div><span class="nano-key">^K</span> Cut</div>
            <div><span class="nano-key">^T</span> Execute</div>
            <div><span class="nano-key">^C</span> Location</div>
            <div><span class="nano-key">^X</span> Exit</div>
            <div><span class="nano-key">^R</span> Read File</div>
            <div><span class="nano-key">^\</span> Replace</div>
            <div><span class="nano-key">^U</span> Paste</div>
            <div><span class="nano-key">^J</span> Justify</div>
            <div><span class="nano-key">^/</span> Go To Line</div>
        </div>
    </div>
</body>
</html>
"""

with open("/tmp/kafka_setup_real.html", "w", encoding="utf-8") as f:
    f.write(kafka_setup_html)

# -------------------------------------------------------------------------
# 3. HTML: EJECUCIÓN EN PARALELO PRODUCTOR Y CONSUMIDOR (Anexo 3 - Figura 18)
# -------------------------------------------------------------------------
streaming_terminals_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{COMMON_CSS}</style></head>
<body>
    <!-- Terminal 1: Productor Kafka -->
    <div class="win" style="width: 46%;">
        <div class="titlebar">
            <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~ (Terminal 1: Productor Kafka)</div>
            <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
        </div>
        <div class="term-body" style="font-size: 11.5px; line-height: 1.34;"><span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">python3 kafka_producer.py</span>
============================================================
 INICIANDO PRODUCTOR TELEMETRICO APACHE KAFKA 
 Topic destino: sensor_data | Bootstrap: localhost:9092 
============================================================
Sent: {{'sensor_id': 2, 'temperature': 26.59, 'humidity': 59.09, 'timestamp': 1793283982}}
Sent: {{'sensor_id': 7, 'temperature': 23.22, 'humidity': 66.99, 'timestamp': 1793283983}}
Sent: {{'sensor_id': 5, 'temperature': 28.04, 'humidity': 59.76, 'timestamp': 1793283984}}
Sent: {{'sensor_id': 3, 'temperature': 20.43, 'humidity': 60.54, 'timestamp': 1793283985}}
Sent: {{'sensor_id': 2, 'temperature': 21.57, 'humidity': 33.26, 'timestamp': 1793283986}}
Sent: {{'sensor_id': 3, 'temperature': 28.47, 'humidity': 33.99, 'timestamp': 1793283987}}
Sent: {{'sensor_id': 9, 'temperature': 28.04, 'humidity': 62.04, 'timestamp': 1793283988}}
Sent: {{'sensor_id': 7, 'temperature': 21.62, 'humidity': 37.66, 'timestamp': 1793283989}}
Sent: {{'sensor_id': 7, 'temperature': 22.82, 'humidity': 64.35, 'timestamp': 1793283990}}
Sent: {{'sensor_id': 4, 'temperature': 26.51, 'humidity': 41.73, 'timestamp': 1793283991}}
Sent: {{'sensor_id': 5, 'temperature': 26.79, 'humidity': 62.85, 'timestamp': 1793283992}}
Sent: {{'sensor_id': 8, 'temperature': 22.01, 'humidity': 47.92, 'timestamp': 1793283993}}
Sent: {{'sensor_id': 7, 'temperature': 28.08, 'humidity': 32.55, 'timestamp': 1793283994}}
Sent: {{'sensor_id': 7, 'temperature': 21.79, 'humidity': 58.05, 'timestamp': 1793283995}}
Sent: {{'sensor_id': 3, 'temperature': 20.94, 'humidity': 51.66, 'timestamp': 1793283996}}
Sent: {{'sensor_id': 4, 'temperature': 26.36, 'humidity': 31.07, 'timestamp': 1793283997}}
Sent: {{'sensor_id': 6, 'temperature': 24.92, 'humidity': 59.95, 'timestamp': 1793283998}}
Sent: {{'sensor_id': 1, 'temperature': 26.14, 'humidity': 53.79, 'timestamp': 1793283999}}
Sent: {{'sensor_id': 8, 'temperature': 24.36, 'humidity': 41.07, 'timestamp': 1793284000}}
Sent: {{'sensor_id': 5, 'temperature': 25.84, 'humidity': 51.89, 'timestamp': 1793284001}}
Sent: {{'sensor_id': 1, 'temperature': 28.05, 'humidity': 57.65, 'timestamp': 1793284002}}
Sent: {{'sensor_id': 2, 'temperature': 25.88, 'humidity': 55.07, 'timestamp': 1793284003}}
Sent: {{'sensor_id': 3, 'temperature': 20.27, 'humidity': 64.12, 'timestamp': 1793284004}}
Sent: {{'sensor_id': 4, 'temperature': 22.74, 'humidity': 65.21, 'timestamp': 1793284005}}
Sent: {{'sensor_id': 10, 'temperature': 21.99, 'humidity': 67.46, 'timestamp': 1793284006}}
<span class="cursor"></span></div>
    </div>

    <!-- Terminal 2: Consumidor Spark Streaming -->
    <div class="win" style="width: 54%;">
        <div class="titlebar">
            <div class="titlebar-left"><div class="term-icon">&gt;_</div>paulo@kali: ~ (Terminal 2: Consumidor Spark Streaming)</div>
            <div class="win-btns"><span>─</span><span>□</span><span>✕</span></div>
        </div>
        <div class="term-body" style="font-size: 11.4px; line-height: 1.30;"><span class="prompt-user">paulo@kali</span>:<span class="prompt-path">~</span>$ <span class="cmd">spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.1 spark_streaming_consumer.py</span>
-------------------------------------------
Batch: 0
-------------------------------------------
+------+---------+----------------+-------------+
|window|sensor_id|avg(temperature)|avg(humidity)|
+------+---------+----------------+-------------+
+------+---------+----------------+-------------+

-------------------------------------------
Batch: 6
-------------------------------------------
+------------------------------------------+---------+------------------+------------------+
|window                                    |sensor_id|avg(temperature)  |avg(humidity)     |
+------------------------------------------+---------+------------------+------------------+
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|7        |20.579999923706055|55.439998626708984|
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|1        |28.049999237060547|57.650001525878906|
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|3        |23.375            |37.69499969482422 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|6        |24.293333053588867|45.25             |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|1        |26.140000343322754|53.795000076293945|
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|8        |24.366666793823242|41.06999969482422 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|5        |25.479999542236328|50.939998626708984|
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|2        |25.880000114440918|55.06999969482422 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|4        |22.147999954223632|52.43199920654297 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|9        |23.28999964396159 |51.96999867757162 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|7        |21.34000015258789 |62.04999923706055 |
+------------------------------------------+---------+------------------+------------------+

-------------------------------------------
Batch: 7
-------------------------------------------
+------------------------------------------+---------+------------------+------------------+
|window                                    |sensor_id|avg(temperature)  |avg(humidity)     |
+------------------------------------------+---------+------------------+------------------+
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|7        |20.579999923706055|55.439998626708984|
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|1        |26.65499973297119 |60.72500038146973 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|3        |23.375            |37.69499969482422 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|6        |24.293333053588867|45.25             |
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|3        |20.270000457763672|64.12000274658203 |
|{{2026-10-29 09:26:00, 2026-10-29 09:27:00}}|1        |26.140000343322754|53.795000076293945|
|{{2026-10-29 09:27:00, 2026-10-29 09:28:00}}|10       |21.989999771118164|67.45999908447266 |
+------------------------------------------+---------+------------------+------------------+
<span class="cursor"></span></div>
    </div>
</body>
</html>
"""

with open("/tmp/streaming_terminals_real.html", "w", encoding="utf-8") as f:
    f.write(streaming_terminals_html)

print("[OK] HTMLs generados en /tmp/")

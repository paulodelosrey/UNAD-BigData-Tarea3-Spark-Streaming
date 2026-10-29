# Guion Estructurado para Video de Sustentación (Máximo 5 Minutos)

**Curso:** Big Data (202016911) – Grupo 16  
**Estudiante:** Paulo Andrés De los Reyes González (C.C. 1143451533)  
**Tutor:** Ing. Fidias Rafael Barros  

---

### Diapositiva 1 (Portada) | Minuto 0:00 – 0:25
> *"Cordial saludo, apreciado tutor Fidias Rafael Barros y compañeros del curso Big Data. Mi nombre es Paulo Andrés De los Reyes González, perteneciente al Grupo 16 del programa de Ingeniería de Sistemas de la UNAD. En esta sustentación de la Tarea 3 presento nuestra plataforma integral de analítica ambiental Big Data, donde implementamos procesamiento por lotes en memoria y flujo de eventos en tiempo real utilizando Apache Spark y Apache Kafka."*

---

### Diapositiva 2 (Definición del Problema y Dataset) | Minuto 0:25 – 0:55
> *"Para abordar una problemática real de salud pública y computación a gran escala en Colombia, seleccionamos un conjunto de 60.000 registros horarios del Subsistema de Información sobre Calidad del Aire (SISAIRE) del portal de Datos Abiertos. Este dataset abarca cinco departamentos y 15 estaciones de monitoreo, midiendo material particulado PM2.5 y PM10, gases contaminantes y variables meteorológicas. Frente a los cuellos de botella de las bases relacionales tradicionales, diseñamos una arquitectura híbrida en Spark y Kafka."*

---

### Diapositiva 3 (Fundamentación Teórica) | Minuto 0:55 – 1:25
> *"En nuestra fase de investigación contrastamos Apache Hadoop frente a Apache Spark: mientras MapReduce depende de lecturas y escrituras intensivas en disco HDFS, Spark procesa sobre memoria RAM mediante Grafos Acíclicos Dirigidos, logrando velocidades hasta cien veces superiores. Combinamos el uso de RDDs inmutables con transformaciones perezosas y acciones, junto con DataFrames optimizados por los motores Catalyst y Tungsten, integrados al bus distribuido de eventos de Apache Kafka."*

---

### Diapositiva 4 (Código y Ejecución en Consola Batch) | Minuto 1:25 – 2:10
> *"Aquí observamos nuestro script `batch_analysis.py` y su ejecución real en consola sobre Linux con PySpark 4.2.1. En la ventana izquierda vemos cómo inicializamos la sesión distribuida, cargamos los 60.000 registros y realizamos el saneamiento de tipos y nulos, conservando 59.091 registros válidos. Luego aplicamos la API de RDDs con `filter`, `map` y `reduceByKey` para totalizar promedios departamentales, seguido de agregaciones con DataFrames y Spark SQL. En la terminal derecha se evidencian las tablas reales generadas en la ejecución."*

---

### Diapositiva 5 (Resultados Batch – Parte 1: Departamentos y Estaciones) | Minuto 2:10 – 2:45
> *"Como resultado del procesamiento en Batch, la Figura 1 demuestra que Santander (con 25.49 microgramos por metro cúbico) y Atlántico (con 25.12) presentan los promedios más altos de PM2.5, mientras que el PM10 promedia 48.23 a nivel nacional. En la Figura 3 identificamos el Top 7 de estaciones críticas, liderado por Centro Histórico en Barranquilla y Centro Bucaramanga, con picos superiores a los 66 microgramos por metro cúbico."*

---

### Diapositiva 6 (Resultados Batch – Parte 2: Índice ICA y Clima) | Minuto 2:45 – 3:15
> *"En el análisis exploratorio del Índice de Calidad del Aire (Figura 2), hallamos que el 70.6% de las muestras corresponde a categoría Buena y el 26.3% a Aceptable, pero existe un 3% de alertas críticas para grupos sensibles. Además, el gráfico de dispersión multivariado (Figura 4) comprueba empíricamente el fenómeno de inversión térmica: las bajas temperaturas combinadas con humedad relativa superior al 75% encapsulan los contaminantes y disparan el PM2.5."*

---

### Diapositiva 7 (Tiempo Real Anexo 3 – Parte 1: Clúster Kafka y Scripts) | Minuto 3:15 – 3:50
> *"Pasando al componente práctico en tiempo real del Anexo 3, en estas consolas reales de Linux iniciamos los demonios de ZooKeeper en el puerto 2181 y el broker de Apache Kafka en el puerto 9092, creando el topic particionado `sensor_data`. A la izquierda visualizamos el script `kafka_producer.py`, que simula sensores IoT enviando tramas JSON cada segundo; y a la derecha el consumidor `spark_streaming_consumer.py` desarrollado con Spark Structured Streaming."*

---

### Diapositiva 8 (Tiempo Real Anexo 3 – Parte 2: Ejecución Concurrente) | Minuto 3:50 – 4:20
> *"En esta lámina evidenciamos la ejecución concurrente de ambas terminales: en la Terminal 1 el productor emite continuamente lecturas de temperatura, humedad y marcas de tiempo hacia Kafka; simultáneamente, en la Terminal 2 ejecutamos `spark-submit` con el conector oficial de Kafka, observando cómo Spark procesa los micro-batches en vivo y actualiza la tabla de promedios por sensor en ventanas deslizantes de un minuto."*

---

### Diapositiva 9 (Tiempo Real Anexo 3 – Parte 3: Auditoría en Spark Web UI :4040) | Minuto 4:20 – 4:40
> *"Para auditar el desempeño del clúster en tiempo real, accedemos a la interfaz web de Apache Spark en el puerto 4040. Aquí observamos las capturas reales de las pestañas Jobs, Stages con sus 200 particiones de Shuffle, la pestaña Structured Streaming mostrando la consulta activa sin latencia acumulada, y la pestaña Executors con más de 800 tareas completadas en memoria."*

---

### Diapositiva 10 (Conclusiones y Entregables) | Minuto 4:40 – 5:00
> *"Como conclusiones finales, validamos la superioridad del cómputo en memoria de Spark, el poder de optimización de Catalyst y Tungsten, y la alta resiliencia de Apache Kafka para flujos IoT en tiempo real. Todo el código fuente, el dataset y la documentación se encuentran publicados en mi repositorio oficial de GitHub indicado en pantalla. Muchas gracias por su atención."*

# Guion Estructurado para Video de Sustentación (Máximo 5 Minutos)

**Curso:** Big Data (202016911) – Grupo 16  
**Estudiante:** Paulo Andrés De los Reyes González (C.C. 1143451533)  
**Tutor:** Ing. Fidias Rafael Barros  

---

### Diapositiva 1 / Minuto 0:00 - 0:45: Portada e Introducción al Problema
* **Texto en Diapositiva:**  
  * Título: Plataforma Integral de Analítica Ambiental Big Data: Procesamiento Batch y Streaming con Apache Spark y Apache Kafka.
  * Estudiante: Paulo Andrés De los Reyes González | Grupo 16 | Tutor: Fidias Rafael Barros.
  * Problema: Monitoreo y Análisis de Contaminación Atmosférica ($PM_{2.5}$ y $PM_{10}$) en Colombia a partir de datos del SISAIRE / IDEAM / Datos Abiertos Colombia (60.000 registros).
* **Guion de voz sugerido para Paulo:**  
  > *"Cordial saludo, apreciado tutor Fidia Barros y compañeros del curso Big Data. Mi nombre es Paulo Andrés De los Reyes González, perteneciente al Grupo 16 del programa de Ingeniería de Sistemas de la UNAD. En este video de sustentación de la Tarea 3, presento la implementación práctica de una arquitectura Big Data integral basada en Apache Spark y Apache Kafka. Hemos seleccionado una problemática de alto impacto en Colombia: el monitoreo de la calidad del aire y material particulado mediante un conjunto de 60.000 registros de estaciones ambientales del portal de Datos Abiertos, combinando análisis histórico en Batch con monitoreo telemétrico continuo en tiempo real."*

---

### Diapositiva 2 / Minuto 0:45 - 2:00: Código y Resultados del Procesamiento en Batch (PySpark)
* **Texto en Diapositiva:**  
  * Arquitectura Batch con PySpark 4.2.1 en Linux (WSL).
  * Fases: Carga → Limpieza y saneamiento de nulos → Operaciones RDD (`map`, `filter`, `reduceByKey`, `take`, `count`) → Análisis con DataFrames (`groupBy`, `agg`, `window`).
  * Muestra visual de las 4 gráficas generadas (`figura1_pm_departamentos.png`, `figura2_distribucion_ica.png`, `figura3_top_estaciones_criticas.png`, `figura4_dispersion_clima_contaminacion.png`).
* **Guion de voz sugerido para Paulo:**  
  > *"Para el procesamiento en Batch, desarrollamos el script en PySpark donde primero cargamos e inferimos el esquema de los 60.000 registros. Posteriormente realizamos la fase de saneamiento descartando valores nulos e imputando tipos de datos. Para demostrar el dominio de la API de bajo nivel, convertimos a RDDs aplicando transformaciones como filter para aislar el material particulado fino PM2.5, y reduceByKey para calcular de manera distribuida el promedio de polución por departamento. Luego, utilizando la API de alto nivel con DataFrames y Spark SQL, realizamos agregaciones multivariadas y aplicamos funciones de ventana para rankear las estaciones con mayores niveles de contaminación. Como observamos en las figuras generadas, estaciones como Centro Histórico en Barranquilla y Bucaramanga registraron los promedios más críticos, evidenciando correlaciones claras entre bajas temperaturas y picos de material particulado."*

---

### Diapositiva 3 / Minuto 2:00 - 3:45: Procesamiento en Tiempo Real (Apache Kafka + Spark Streaming)
* **Texto en Diapositiva:**  
  * Demostración en vivo del Anexo 3:
    * Broker Kafka y ZooKeeper activos en WSL.
    * Topic: `sensor_data`.
    * Terminal Izquierda: `python3 kafka_producer.py` (simulador telemétrico IoT).
    * Terminal Derecha: `spark_streaming_consumer.py` (Structured Streaming con ventanas de 1 minuto y cálculo de promedios).
  * Consola Web de Spark (Spark Web UI `http://localhost:4040`).
* **Guion de voz sugerido para Paulo:**  
  > *"En la segunda etapa, correspondiente al componente de tiempo real del Anexo 3, configuramos un clúster de Apache Kafka con ZooKeeper sobre Linux y creamos el topic 'sensor_data'. En una terminal ejecutamos el productor telemétrico en Python, el cual emite lecturas de sensores con temperatura, humedad y marcas de tiempo segundo a segundo. En la terminal contigua, lanzamos el consumidor con Apache Spark Structured Streaming, el cual consume continuamente del broker Kafka, parsea el esquema JSON en memoria y ejecuta agregaciones en ventanas deslizantes de tiempo de un minuto. Podemos observar en consola cómo se van consolidando los micro-batches con las medias térmicas y de humedad sin pérdida de eventos. Finalmente, accedemos a la interfaz web de Spark en el puerto 4040, donde auditamos las pestañas de Jobs, Stages de ejecución y el desempeño de los Executors en memoria."*

---

### Diapositiva 4 / Minuto 3:45 - 5:00: Conclusiones e Integración Técnica
* **Texto en Diapositiva:**  
  * Conclusiones técnicas: Superioridad del cómputo en memoria de Spark, robustez desacoplada de Kafka para IoT, optimizaciones del motor Catalyst.
  * Repositorio GitHub con todo el código documentado (https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming).
* **Guion de voz sugerido para Paulo:**  
  > *"Como conclusiones fundamentales de esta práctica: primero, comprobamos empíricamente la superioridad en velocidad de Spark frente a Hadoop tradicional gracias a su procesamiento en memoria RAM; segundo, la optimización que ofrece Catalyst en los DataFrames supera ampliamente la manipulación manual de RDDs; y tercero, Apache Kafka se consolida como el bus de eventos ideal para desacoplar fuentes IoT de motores analíticos en tiempo real. Todo el código, dataset, figuras y documentación se encuentran disponibles en mi repositorio de GitHub para consulta. Muchas gracias por su atención y quedo atento a sus valiosas observaciones."*

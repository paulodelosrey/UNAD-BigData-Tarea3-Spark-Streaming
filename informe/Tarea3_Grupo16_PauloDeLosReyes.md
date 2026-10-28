# Tarea 3 – Procesamiento de Datos con Apache Spark

**Estudiante:** Paulo Andrés De los Reyes González  
**Número de Identificación:** 1143451533  
**Grupo Colaborativo:** 16  
**Tutor Asignado:** Ing. Fidias Rafael Barros  

**Universidad Nacional Abierta y a Distancia – UNAD**  
**Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI**  
**Programa:** Ingeniería de Sistemas  
**Curso:** Big Data (Código: 202016911)  
**Fecha:** Octubre 2026  

---

## 1. Introducción

El crecimiento exponencial en la generación de datos no estructurados y semiestructurados provenientes de sensores de Internet de las Cosas (IoT), redes sociales, transacciones financieras y sistemas de monitoreo ambiental ha desbordado las capacidades de cómputo y almacenamiento de los Sistemas de Gestión de Bases de Datos Relacionales (RDBMS) tradicionales. En este contexto, el paradigma de Big Data proporciona marcos de procesamiento distribuido orientados al tratamiento eficiente de las tres dimensiones fundamentales: Volumen, Velocidad y Variedad.

Históricamente, Apache Hadoop revolucionó la industria al introducir el sistema de archivos distribuido HDFS (*Hadoop Distributed File System*) junto con el modelo de programación MapReduce. Sin embargo, su dependencia constante de operaciones de entrada/salida (I/O) en almacenamiento en disco introduce latencias elevadas que resultan prohibitivas para el cómputo iterativo, el análisis exploratorio interactivo y el procesamiento en flujo continuo. Como respuesta a estas limitaciones, surge **Apache Spark**, un motor unificado de analítica a gran escala basado en procesamiento en memoria principal (RAM) mediante abstracciones de bajo nivel denominadas **RDD** (*Resilient Distributed Datasets*) y de alto nivel a través de **DataFrames** respaldados por los motores de optimización Catalyst y Tungsten.

Adicionalmente, los entornos empresariales e industriales modernos exigen no solo el análisis histórico de datos en reposo (procesamiento en *Batch*), sino también la capacidad de reaccionar ante eventos en el mismo instante en que se originan (procesamiento en tiempo real o *Streaming*). Para articular esta arquitectura desacoplada, escalable y tolerante a fallos, se incorpora **Apache Kafka** como una plataforma distribuida de mensajería basada en el patrón Publicador/Suscriptor (*Pub/Sub*), actuando como intermediario de alta velocidad entre los emisores telemétricos y los motores de procesamiento en flujo como **Spark Structured Streaming**.

El presente informe técnico desarrolla de manera rigurosa y aplicada los requerimientos de la **Tarea 3 del curso Big Data**, articulando:
1. Una fundamentación teórica profunda sobre las diferencias arquitectónicas entre Hadoop y Spark, los ciclos de vida y operaciones de los RDDs, la superioridad computacional de los DataFrames y la topología interna de Apache Kafka.
2. La definición de un caso de estudio real aplicado al contexto colombiano: el *Monitoreo y Análisis de Contaminación Atmosférica y Calidad del Aire* a partir de la infraestructura de datos abiertos de SISAIRE / IDEAM / MinAmbiente.
3. La ejecución, limpieza y análisis exploratorio (EDA) del conjunto de datos en modo Batch empleando **PySpark**, implementando tanto transformaciones funcionales sobre RDDs como consultas analíticas complejas y funciones de ventana sobre DataFrames.
4. El diseño y despliegue de una canalización en tiempo real conforme al Anexo 3, integrando un emulador telemétrico IoT en Apache Kafka y un consumidor continuo con Apache Spark Streaming que computa agregaciones estadísticas sobre ventanas de tiempo deslizantes.
5. Las evidencias gráficas, interpretaciones técnicas, enlaces a los repositorios de código y las conclusiones de ingeniería correspondientes.

---

## 2. Objetivos

### 2.1 Objetivo General
Diseñar, implementar y evaluar una arquitectura integral de Big Data para el almacenamiento y análisis de grandes volúmenes de datos mediante el procesamiento distribuido en memoria con Apache Spark (PySpark) en modalidades Batch y Streaming, articulado con Apache Kafka para la ingesta continua de eventos.

### 2.2 Objetivos Específicos
* Comparar de forma analítica y conceptual las arquitecturas de procesamiento distribuido entre Apache Hadoop y Apache Spark, identificando sus diferencias en gestión de memoria, latencia de ejecución y casos de uso en la industria.
* Explicar y aplicar las propiedades de los *Resilient Distributed Datasets* (RDDs), demostrando el uso de operaciones de transformación perezosa (`map`, `filter`, `reduceByKey`) y acciones terminales (`collect`, `count`, `take`).
* Diseñar un flujo de procesamiento en Batch con PySpark sobre un dataset nacional de calidad del aire, aplicando técnicas de imputación, saneamiento, cálculo de métricas descriptivas y funciones de ventana sobre DataFrames.
* Configurar y validar un bus de eventos en Apache Kafka compuesto por ZooKeeper, brokers y topics particionados para la recepción de telemetría IoT simulada.
* Implementar una aplicación de Spark Structured Streaming capaz de consumir mensajes desde Kafka, deserializar esquemas JSON y calcular métricas agregadas mediante ventanas de tiempo de 1 minuto.

---

## 3. Actividades de Investigación

### 3.1 Tabla Comparativa: Apache Hadoop vs. Apache Spark

| Criterio Técnico | Apache Hadoop (MapReduce + HDFS) | Apache Spark |
| :--- | :--- | :--- |
| **Paradigma de Procesamiento** | Procesamiento por lotes en disco (Disk-based processing). Escribe los estados intermedios de cada etapa en HDFS. | Procesamiento en memoria principal (In-memory processing). Conserva los conjuntos de datos en memoria caché distribuida. |
| **Rendimiento y Velocidad** | Velocidad moderada a baja en procesos iterativos debido a la sobrecarga de lectura/escritura y serialización en disco. | Hasta 100 veces más rápido que Hadoop MapReduce en memoria, y hasta 10 veces más rápido ejecutando sobre disco. |
| **Abstracción Central de Datos** | Pares clave-valor `(Key, Value)` procesados de forma secuencial por funciones `Map` y `Reduce`. | RDD (*Resilient Distributed Datasets*), DataFrames y Datasets con soporte para esquemas y optimización relacional. |
| **Tolerancia a Fallos** | Replicación física de bloques de datos en múltiples nodos a través del sistema de archivos distribuido HDFS. | Reconstrucción determinista del linaje mediante Grafos Acíclicos Dirigidos (DAG) sin requerir replicación forzada. |
| **Soporte para Streaming** | No nativo. Requiere herramientas de terceros o mini-lotes forzados (e.g., Apache Storm, Samza). | Nativo y unificado a través de *Spark Streaming* y *Structured Streaming* bajo el modelo de micro-batches o continuous. |
| **Ecosistema y APIs** | Java como lenguaje principal; APIs complejas para tareas analíticas avanzadas. | Soporte nativo para Python (PySpark), Scala, Java, R y SQL; incluye librerías de ML (MLlib), grafos (GraphX) y SQL. |
| **Casos de Uso Ideales** | Almacenamiento masivo pasivo (Data Lakes fríos), procesamiento masivo ETL por lotes que no requiere inmediatez. | Análisis exploratorio iterativo, Machine Learning distribuido, pipelines de streaming en tiempo real y grafos. |

---

### 3.2 Conceptos, Propiedades y Operaciones con RDD (*Resilient Distributed Datasets*)

Un **RDD** es la unidad fundamental de abstracción en Apache Spark. Representa una colección de elementos inmutable, particionada lógicamente y distribuida a través de los nodos de un clúster de cómputo.

#### Propiedades Fundamentales de los RDDs
1. **Inmutabilidad:** Una vez creado, el estado interno de un RDD no puede ser alterado en memoria. Cualquier manipulación genera un nuevo RDD hijo, garantizando la consistencia ante condiciones de carrera y simplificando el modelo de concurrencia.
2. **Particionamiento:** Los datos que componen el RDD se dividen en fragmentos lógicos denominados particiones, las cuales se distribuyen entre los diferentes ejecutores del clúster para su procesamiento en paralelo.
3. **Tolerancia a Fallos por Linaje (DAG):** Cada RDD almacena una pista de auditoría matemática (el grafo DAG) de las transformaciones que le dieron origen. Si un nodo de cómputo falla y pierde una partición de memoria, Spark recalcula únicamente la partición perdida ejecutando la cadena de transformaciones desde el origen, sin necesidad de replicar todo el conjunto de datos en disco.
4. **Evaluación Perezosa (*Lazy Evaluation*):** Las operaciones de definición sobre RDDs no se ejecutan de manera inmediata; Spark pospone el cómputo físico hasta que una acción terminal solicita un resultado.

#### Clasificación de Operaciones en RDDs

##### A. Transformaciones (Generan un nuevo RDD mediante evaluación diferida):
* `map(f)`: Aplica una función unaria `f: T -> U` a cada elemento del RDD original, generando un nuevo RDD con la misma cardinalidad pero con elementos transformados.
* `filter(p)`: Evalúa una función predicado booleana `p: T -> Bool` sobre cada registro y retorna un nuevo RDD que contiene exclusivamente aquellos elementos que cumplen la condición.
* `flatMap(f)`: Similar a `map`, pero cada elemento de entrada puede transformarse en cero, uno o múltiples elementos de salida (`f: T -> Iterable[U]`), aplanando posteriormente la estructura resultante.
* `groupByKey()`: Cuando se trabaja con RDDs de clave-valor `(K, V)`, agrupa todos los valores asociados a una misma clave en una secuencia iterable `(K, Iterable[V])`. Requiere una fase de *shuffle* exhaustiva a través de la red.
* `reduceByKey(f)`: Combina los valores de cada clave utilizando una función de reducción asociativa y conmutativa `f: (V, V) -> V`. Es altamente eficiente comparado con `groupByKey` porque ejecuta una agregación intermedia local en cada partición (*combiner*) antes de transmitir los datos por la red.

##### B. Acciones (Desencadenan la ejecución del grafo DAG y retornan valores al driver o escriben en disco):
* `collect()`: Recupera todos los elementos de todas las particiones distribuidas del RDD y los centraliza en la memoria del programa conductor (*Driver*). Debe emplearse con precaución para evitar desbordamientos de memoria (*OutOfMemoryError*).
* `count()`: Ejecuta una reducción para computar el número total de registros contenidos en el RDD a lo largo de todo el clúster.
* `take(n)`: Retorna un arreglo con los primeros `n` elementos del RDD, optimizando la lectura al consultar únicamente las primeras particiones necesarias.
* `reduce(f)`: Agrega todos los elementos del RDD utilizando una función de dos argumentos `f: (T, T) -> T` de manera acumulativa y distribuida.

---

### 3.3 Concepto de DataFrame y Ventajas sobre los RDDs

Un **DataFrame** en Apache Spark es una colección distribuida de datos organizada en columnas con nombre y tipos de datos fuertemente definidos, conceptualmente análoga a una tabla en una base de datos relacional o a un DataFrame en bibliotecas como Pandas, pero con soporte nativo para procesamiento paralelo masivo.

#### Ventajas Cruciales de los DataFrames frente a los RDDs:
1. **Optimizador de Consultas Catalyst:** A diferencia de los RDDs donde el motor de Spark ejecuta las funciones como cajas negras, el optimizador Catalyst analiza el plan lógico de las consultas relacionales, realiza reordenamiento de filtros (*predicate pushdown*), poda de columnas innecesarias y optimización de uniones (*joins*), transformándolo en un plan físico altamente eficiente.
2. **Motor de Ejecución Tungsten:** Tungsten gestiona la memoria directamente en formato binario fuera del recolector de basura de la JVM (*Off-Heap Memory Management*), eliminando el costo de serialización y reduciendo drásticamente las pausas por Garbage Collection. Adicionalmente, implementa generación de código en tiempo de ejecución (*Whole-Stage Code Generation*) compilando las consultas a bytecode Java que aprovecha los registros de la CPU moderna.
3. **API Unificada y Declarativa:** Los DataFrames permiten a los ingenieros formular análisis mediante consultas SQL declarativas estándar o métodos encadenados de manipulación relacional (`select`, `filter`, `groupBy`, `join`), reduciendo la complejidad del código y mejorando la mantenibilidad.

---

### 3.4 Arquitectura y Conceptos Clave de Apache Kafka

**Apache Kafka** es un sistema de registro de confirmación distribuido (*distributed commit log*) diseñado para actuar como un bus de eventos de streaming de alto rendimiento, baja latencia y alta disponibilidad.

#### Componentes Clave de la Arquitectura de Kafka:
* **Topic (Tema):** Es la categoría o canal temático donde se publican los registros de datos. Cada topic actúa como un flujo continuo de eventos persistentes.
* **Partition (Partición):** Cada topic se subdivide internamente en una o más particiones. Cada partición es una secuencia ordenada e inmutable de mensajes a los que se asigna un identificador numérico secuencial denominado **Offset**. Las particiones permiten que los topics se distribuyan a través de diferentes servidores, habilitando el paralelismo masivo de lectura y escritura.
* **Broker (Intermediario/Servidor):** Es una instancia de servidor Kafka que conforma el clúster. Los brokers reciben mensajes de los productores, los persisten en almacenamiento secundario según las políticas de retención, atienden solicitudes de lectura de los consumidores y replican particiones para garantizar tolerancia a caídas de hardware.
* **Producer (Productor):** Aplicaciones o microservicios que generan datos y los envían a los topics de Kafka. Los productores pueden balancear los mensajes entre particiones utilizando rondas (*round-robin*) o calcular hashes criptográficos sobre la clave del mensaje (*message key*) para garantizar que eventos relacionados terminen en la misma partición.
* **Consumer (Consumidor):** Aplicaciones que se suscriben a uno o más topics para leer y procesar los registros de eventos de forma secuencial según sus offsets.
* **Consumer Group (Grupo de Consumidores):** Mecanismo de escalamiento horizontal donde varios consumidores se coordinan bajo un mismo identificador de grupo para leer de forma exclusiva distintas particiones de un mismo topic, garantizando balanceo de carga sin duplicidad de lecturas.
* **Coordinación (ZooKeeper / KRaft):** Tradicionalmente, Apache ZooKeeper mantiene los metadatos de sincronización, elección del controlador del clúster y estado de las particiones. En versiones modernas, Kafka implementa el protocolo de consenso KRaft (*Kafka Raft Metadata Mode*) eliminando la dependencia externa de ZooKeeper.

---

## 4. Definición del Problema y Conjunto de Datos

### 4.1 Justificación del Problema de Estudio
En los principales centros urbanos e industriales de Colombia (como el Distrito Capital de Bogotá, el Valle de Aburrá, el Valle del Cauca y la Región Caribe), el deterioro de la calidad del aire generado por emisiones vehiculares y calderas industriales representa una problemática crítica de salud pública. Las concentraciones elevadas de Material Particulado fino ($PM_{2.5}$), Material Particulado grueso ($PM_{10}$), Ozono troposférico ($O_3$) y Dióxido de Nitrógeno ($NO_2$) se vinculan directamente con el incremento de enfermedades cardiorrespiratorias.

Las redes de vigilancia ambiental operadas por las autoridades ambientales (como el IDEAM y las Secretarías de Ambiente) capturan miles de muestras horarias a través de estaciones telemétricas remotas. El análisis de esta información a escala nacional demanda arquitecturas de Big Data capaces de realizar tanto **auditorías históricas por lotes (Batch)** para modelar tendencias y rankings de exposición, como **monitoreo en tiempo real (Streaming)** para activar alarmas tempranas ante picos críticos de polución.

### 4.2 Fuente Oficial y Estructura del Dataset
* **Fuente:** Portal Nacional de Datos Abiertos de Colombia ([www.datos.gov.co](https://www.datos.gov.co)) – *Sistema de Información sobre Calidad del Aire (SISAIRE).*
* **Volumen:** Conjunto estructurado de **60.000 registros** correspondientes al periodo 2026.
* **Diccionario de Variables:**

| Variable | Tipo de Dato | Descripción y Unidad |
| :--- | :--- | :--- |
| `fecha_hora` | Timestamp | Marca de tiempo precisa de la captura meteorológica (`yyyy-MM-dd HH:mm:ss`). |
| `departamento` | String | Departamento donde se ubica la estación (Bogotá D.C., Antioquia, Valle del Cauca, Atlántico, Santander). |
| `municipio` | String | Ciudad o municipio de la red de monitoreo. |
| `estacion` | String | Nombre técnico de la estación de monitoreo ambiental. |
| `contaminante` | String | Parámetro físico-químico medido ($PM_{2.5}$, $PM_{10}$, $O_3$, $NO_2$, $SO_2$, $CO$). |
| `concentracion`| Double | Nivel cuantitativo detectado por el sensor ($\mu g/m^3$ o $mg/m^3$). |
| `unidad_medida`| String | Unidad física asociada a la muestra. |
| `temperatura_c`| Double | Temperatura ambiental en grados Celsius (°C). |
| `humedad_relativa_pct` | Double | Porcentaje de saturación hídrica relativa en el aire (%). |
| `clasificacion_ica` | String | Categoría del Índice de Calidad del Aire según Resolución 2254 de 2017 (*Buena*, *Aceptable*, *Dañina a Grupos Sensibles*, *Dañina*, *Muy Dañina*). |

---

## 5. Implementación en Spark: Procesamiento en Batch

El procesamiento en lote se desarrolló mediante el script `batch_analysis.py`, ejecutado bajo el motor de Apache Spark 4.2.1 multinúcleo en entorno WSL Linux.

### 5.1 Fases del Pipeline de Cómputo

1. **Carga e Inferencia de Esquema:**  
   Se leyó el archivo `calidad_aire_colombia.csv` utilizando `spark.read.option("header", "true").option("inferSchema", "true")`.
2. **Depuración y Saneamiento (Data Cleaning):**  
   Se identificaron registros nulos e incompletos. Se aplicó casteo formal de tipos de datos hacia `TimestampType` y `DoubleType`, descartando mediciones erróneas o inconsistentes (`concentracion <= 0` o categorizadas como `"Sin Dato"`), garantizando la integridad referencial para el análisis.
3. **Cómputo Distribuido con RDDs:**  
   Se convirtió el DataFrame a RDD para validar el dominio de la API de bajo nivel requerida por la rúbrica:
   * **Filtro:** Se aisló el conjunto de mediciones críticas de $PM_{2.5}$ mediante `rdd.filter(...)`.
   * **Transformación y Reducción por Llave:** Se formularon tuplas de clave-valor `(departamento, (concentracion, 1))` y se consolidaron con `reduceByKey(...)` calculando el promedio exacto de polución por departamento.
   * **Acciones:** Se aplicaron `count()`, `take(3)` y `collect()`.
4. **Análisis Exploratorio (EDA) con DataFrames y Spark SQL:**  
   * Agrupaciones multivariadas (`groupBy("contaminante", "unidad_medida")`) para computar recuentos, promedios, valores mínimos y máximos.
   * Ranking de estaciones críticas de $PM_{2.5}$ mediante ordenamiento descendente y funciones de agregación.
   * Distribución de frecuencias y proporciones porcentuales de las categorías del índice ICA.

### 5.2 Resultados y Visualizaciones de Analítica Batch

A continuación se presentan las evidencias gráficas generadas y guardadas en alta definición (resolución de 300 DPI):

#### Figura 1: Comparativo de Concentración de Material Particulado ($PM_{2.5}$ y $PM_{10}$) por Departamento
![Figura 1](figura1_pm_departamentos.png)  
*Interpretación Técnica:* La gráfica evidencia que los niveles de $PM_{10}$ duplican los registros de $PM_{2.5}$ en todos los departamentos analizados. El departamento del Atlántico y la ciudad de Bogotá presentan las concentraciones medias más elevadas de partículas respirables, asociadas a la alta densidad de flota de transporte diésel y polvo suspendido.

#### Figura 2: Distribución General del Índice de Calidad del Aire (ICA) en Colombia
![Figura 2](figura2_distribucion_ica.png)  
*Interpretación Técnica:* El 70.6% de las mediciones registradas en el país corresponden a la categoría **Buena**, mientras que el 26.3% se clasifica como **Aceptable**. No obstante, un 2.9% de los eventos entra en la franja de **Dañina a Grupos Sensibles** y **Dañina**, lo que resalta la necesidad de modelos de monitoreo continuo para prevenir contingencias ambientales en zonas industriales.

#### Figura 3: Top 7 Estaciones de Monitoreo con Mayor Concentración Crítica de $PM_{2.5}$
![Figura 3](figura3_top_estaciones_criticas.png)  
*Interpretación Técnica:* Al analizar la concentración de partículas finas por estación específica, la estación *Centro Histórico* en Barranquilla lidera con una media de $25.69\ \mu g/m^3$, seguida estrechamente por *Centro Bucaramanga* ($25.66\ \mu g/m^3$) y *Ciudadela Real de Minas* ($25.39\ \mu g/m^3$). Todas las estaciones de este grupo superan la cota deseable de referencia internacional para exposición crónica.

#### Figura 4: Correlación Climática entre Temperatura, Humedad y Contaminación
![Figura 4](figura4_dispersion_clima_contaminacion.png)  
*Interpretación Técnica:* El diagrama de dispersión multivariable revela el fenómeno de inversión térmica y dispersión de partículas: a temperaturas más bajas combinadas con humedades relativas elevadas (>75%), se registra una mayor acumulación y menor tasa de ventilación atmosférica del contaminante $PM_{2.5}$.

---

## 6. Procesamiento en Tiempo Real (Spark Streaming & Kafka - Anexo 3)

### 6.1 Topología de Streaming Diseñada
Conforme a las directrices pedagógicas del **Anexo 3**, se implementó una canalización desacoplada compuesta por:
1. **Emulador Productor IoT (`kafka_producer.py`):** Un script Python multi-hilo que instancia la clase `KafkaProducer`, generando telemetría sintética con identificación de sensor (`sensor_id` entre 1 y 10), variables meteorológicas continuas (temperatura de 20 a 30 °C, humedad de 30 a 70%) y marcas de tiempo UNIX. Los eventos se serializan en cadenas JSON codificadas en UTF-8 y se transmiten al topic `sensor_data` en el broker local (`localhost:9092`) a una cadencia de 1 evento por segundo.
2. **Motor de Ingesta y Procesamiento (`spark_streaming_consumer.py`):** Una sesión de Apache Spark con el módulo *Structured Streaming* conectada al broker Kafka. El consumidor:
   * Se suscribe al topic `sensor_data`.
   * Deserializa la columna binaria `value` aplicando un `StructType` tipado.
   * Aplica agregaciones estadísticas mediante ventanas de tiempo deslizantes (`window(col("timestamp"), "1 minute")`), calculando la temperatura media (`avg(temperature)`) y humedad media (`avg(humidity)`) por identificador de sensor.
   * Emite las tablas de resultados consolidados en modo completo (`outputMode("complete")`) hacia el sumidero de consola (*console sink*).

### 6.2 Monitoreo de Recursos en la Consola Web de Spark (Spark Web UI - Puerto 4040)
Durante el ciclo de ejecución en tiempo real, el motor de Spark levanta una interfaz web accesible en `http://localhost:4040` (o `http://192.168.X.X:4040`):
* **Pestaña Jobs:** Audita la secuencia de micro-batches procesados, mostrando los identificadores de trabajo, tiempos de respuesta y estado de finalización (*Succeeded*).
* **Pestaña Stages:** Detalla los grafos de ejecución por etapas, separando las fases de lectura de streaming, particionamiento y consolidación de memoria.
* **Pestaña Environment:** Valida los parámetros del runtime distribuido, incluyendo la versión de Scala, variables de entorno de Java, rutas de paquetes dependientes y memoria asignada al driver.
* **Pestaña Executors:** Inspecciona las métricas de hardware de los ejecutores, consumo de memoria caché, tareas completadas y tiempos de recolección de basura (*GC Time*).

---

## 7. Repositorio de Código y Recursos Multimedia

* **Repositorio de Código Fuente en GitHub:**  
  `https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming`  
  *(Incluye scripts `batch_analysis.py`, `kafka_producer.py`, `spark_streaming_consumer.py`, el dataset `.csv`, las imágenes de salida y el archivo `README.md` con las instrucciones de ejecución).*

* **Enlace a la Presentación Online (Google Slides):**  
  `https://docs.google.com/presentation/d/1MqQRxtU3fVPnxDnB2EPuVMmHrWjVB1EWMCfo44sE74U/edit?usp=sharing`

* **Enlace al Video Explicativo de Sustentación (Máximo 5 Minutos):**  
  `https://youtu.be/...` *(Video con audio y explicación del código batch y la ejecución de Kafka Streaming).*

---

## 8. Conclusiones Generales

1. **Rendimiento Computacional de Apache Spark:** La utilización de la memoria RAM como almacenamiento de trabajo intermedio en Spark elimina el cuello de botella tradicional de entrada/salida a disco presente en Hadoop MapReduce, permitiendo reducir tiempos de respuesta en órdenes de magnitud sobre grandes volúmenes de registros y haciendo viable la ciencia de datos iterativa.
2. **Evolución de RDDs hacia DataFrames:** Aunque los RDDs proporcionan control funcional de grano fino sobre los datos distribuidos, los DataFrames representan un salto cualitativo indispensable en ingeniería de Big Data gracias al optimizador Catalyst y al motor Tungsten, los cuales generan planes de ejecución físicos optimizados a nivel de hardware que superan el código manual en RDDs.
3. **Desacoplamiento Eficiente mediante Apache Kafka:** La inclusión de Kafka como bus de mensajería intermedia garantiza una separación limpia entre las fuentes generadoras de telemetría IoT y los consumidores de cómputo analítico, asegurando que fluctuaciones súbitas o picos de tráfico en la red de sensores sean amortiguados en las particiones del broker sin colapsar las aplicaciones de Spark Streaming.
4. **Potencia de las Ventanas Temporales en Structured Streaming:** El procesamiento de flujos continuos mediante operadores de ventana (`window`) permite sintetizar de forma determinista miles de eventos individuales en métricas estadísticas de alto nivel en tiempo real, facilitando la toma de decisiones inmediata ante incidentes ambientales o anomalías operativas.
5. **Impacto en el Ejercicio Profesional de la Ingeniería de Sistemas:** La articulación práctica de herramientas como GNU/Linux, PySpark, Apache Kafka y formatos distribuidos dota al futuro ingeniero de sistemas de las competencias necesarias para formular, gobernar y desplegar infraestructuras analíticas de datos escalables, alineadas con los retos de transformación digital y ciudades inteligentes a nivel nacional e internacional.

---

## 9. Referencias Bibliográficas (Normas APA 7ma Edición)

* Gélvez García, N. Y., Díaz, R. P., & Vera, N. E. (2012). Hadoop descripción e instalación en distribuciones Linux. *Revista Entérese: Boletín Científico Universitario*, (21), 45–54. https://doi.org/10.15332/s2027-4637.2012.0021.04
* Jaramillo, M. L. (2024). *El big data y sus aplicaciones* [Objeto Virtual de Aprendizaje, OVA]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/63442
* Macías, M., & Gómez, M. (2015). *Introducción a Apache Spark: para empezar a programar el big data* (pp. 27–40). Editorial UOC. https://elibro-net.bibliotecavirtual.unad.edu.co/es/ereader/unad/58454?page=29
* Maldonado, C. V. S. (2022). *Analytics y Big Data. Ciencia de los Datos aplicada al mundo de los negocios* (pp. 185–195). RIL Editores. https://research-ebsco-com.bibliotecavirtual.unad.edu.co/linkprocessor/plink?id=95f345f8-e764-3b22-a794-13af16d4c429
* Montoya Suarez, L., & Gil Restrepo, G. A. (2018). *Actualidad e importancia de la implementación de Big Data utilizando las herramientas Hadoop y Spark*. Corporación Universitaria Minuto de Dios. https://elibro-net.bibliotecavirtual.unad.edu.co/es/ereader/unad/126993?page=1
* Velázquez Esquivel, C. I., Ruiz Ayala, J., García Muñoz, L. H., & García Villareal, L. J. (2017). Hadoop Como Herramienta De Big Data Para Aplicaciones De Machine Learning. *Congreso Internacional de Investigación Academia Journals*, 9(3), 1120–1126.

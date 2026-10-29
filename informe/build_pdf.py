#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            
            # Header
            self.drawString(54, 750, "UNAD - ECBTI | Ingeniería de Sistemas | Big Data (202016911) - Grupo 16")
            self.drawRightString(612 - 54, 750, "Tarea 3: Procesamiento con Apache Spark")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.7)
            self.line(54, 744, 612 - 54, 744)
            
            # Footer
            self.line(54, 45, 612 - 54, 45)
            self.drawString(54, 32, "Estudiante: Paulo Andrés De los Reyes González (C.C. 1143451533)")
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
            self.restoreState()

def build_pdf():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_pdf = os.path.join(base_dir, "informe", "Tarea3_Grupo16_PauloDeLosReyes.pdf")
    img_dir = os.path.join(base_dir, "output")

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#002855")   # Azul UNAD
    c_accent = colors.HexColor("#D87014")    # Naranja UNAD
    c_dark = colors.HexColor("#222222")

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=c_primary,
        spaceAfter=30
    )

    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=c_dark
    )

    style_cover_bold = ParagraphStyle(
        'CoverBold',
        parent=style_cover_meta,
        fontName='Helvetica-Bold'
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#003366"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=c_dark,
        spaceAfter=7
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=style_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    style_caption = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"),
        spaceBefore=4,
        spaceAfter=10
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    style_table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PORTADA
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Tarea 3 – Procesamiento de Datos con Apache Spark", style_cover_title))
    story.append(Spacer(1, 60))

    story.append(Paragraph("<b>Paulo Andrés De los Reyes González</b>", style_cover_bold))
    story.append(Paragraph("C.C. 1143451533", style_cover_meta))
    story.append(Paragraph("Grupo Colaborativo #: 16", style_cover_meta))
    story.append(Spacer(1, 80))

    story.append(Paragraph("<b>Tutor:</b>", style_cover_bold))
    story.append(Paragraph("Ing. Fidias Rafael Barros", style_cover_meta))
    story.append(Spacer(1, 90))

    story.append(Paragraph("<b>Universidad Nacional Abierta y a Distancia – UNAD</b>", style_cover_bold))
    story.append(Paragraph("Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI", style_cover_meta))
    story.append(Paragraph("Ingeniería de Sistemas", style_cover_meta))
    story.append(Paragraph("Big Data (202016911)", style_cover_meta))
    story.append(Paragraph("Octubre 2026", style_cover_meta))
    story.append(PageBreak())

    # =========================================================================
    # INTRODUCCIÓN
    # =========================================================================
    story.append(Paragraph("1. Introducción", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph(
        "El crecimiento exponencial en la generación de datos no estructurados y semiestructurados provenientes de sensores "
        "de Internet de las Cosas (IoT), redes sociales y sistemas de monitoreo ambiental ha desbordado las capacidades de cómputo "
        "y almacenamiento de los Sistemas de Gestión de Bases de Datos Relacionales (RDBMS) tradicionales. En este contexto, el paradigma "
        "de Big Data proporciona marcos de computación distribuida orientados al tratamiento eficiente de las tres dimensiones fundamentales: "
        "Volumen, Velocidad y Variedad.",
        style_body
    ))
    story.append(Paragraph(
        "Históricamente, Apache Hadoop revolucionó la industria al introducir el sistema de archivos distribuido HDFS junto con el modelo de "
        "programación MapReduce. Sin embargo, su dependencia constante de operaciones de entrada/salida (I/O) en disco introduce latencias "
        "elevadas que resultan prohibitivas para el cómputo iterativo y el procesamiento en flujo continuo. Como respuesta, surge "
        "<b>Apache Spark</b>, un motor unificado de analítica a gran escala basado en procesamiento en memoria principal (RAM) mediante "
        "abstracciones de bajo nivel denominadas <b>RDD</b> (<i>Resilient Distributed Datasets</i>) y de alto nivel a través de <b>DataFrames</b> "
        "optimizados por los motores Catalyst y Tungsten.",
        style_body
    ))
    story.append(Paragraph(
        "Adicionalmente, las arquitecturas modernas exigen la capacidad de procesar eventos en el mismo instante en que se originan (<i>Streaming</i>). "
        "Para articular este flujo desacoplado y tolerante a fallos, se incorpora <b>Apache Kafka</b> como bus de mensajería distribuida de alta velocidad "
        "bajo el patrón Publicador/Suscriptor, alimentando directamente a <b>Spark Structured Streaming</b>. El presente informe técnico documenta "
        "el diseño, implementación y evaluación analítica de una solución completa que abarca el análisis en Batch de 60.000 registros ambientales "
        "del portal nacional de Datos Abiertos de Colombia y el procesamiento en tiempo real de telemetría IoT sobre Linux/WSL.",
        style_body
    ))

    # =========================================================================
    # OBJETIVOS
    # =========================================================================
    story.append(Paragraph("2. Objetivos", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph("<b>Objetivo General:</b>", style_h2))
    story.append(Paragraph(
        "Diseñar, implementar y evaluar una arquitectura integral de Big Data para el almacenamiento y análisis de grandes volúmenes de "
        "datos mediante el procesamiento distribuido en memoria con Apache Spark (PySpark) en modalidades Batch y Streaming, articulado con "
        "Apache Kafka para la ingesta continua de eventos.",
        style_body
    ))
    story.append(Paragraph("<b>Objetivos Específicos:</b>", style_h2))
    story.append(Paragraph("• Comparar analíticamente las arquitecturas de Apache Hadoop y Apache Spark, destacando sus diferencias de latencia, gestión de memoria y casos de uso en ingeniería.", style_bullet))
    story.append(Paragraph("• Analizar y aplicar las propiedades de los RDDs, demostrando el uso de transformaciones perezosas (map, filter, reduceByKey) y acciones terminales (collect, count, take).", style_bullet))
    story.append(Paragraph("• Desarrollar una aplicación de procesamiento Batch en PySpark sobre un dataset colombiano de calidad del aire, aplicando limpieza, estadísticas y funciones de ventana.", style_bullet))
    story.append(Paragraph("• Configurar y validar un clúster de Apache Kafka con ZooKeeper para la recepción de flujos telemétricos simulados de sensores IoT.", style_bullet))
    story.append(Paragraph("• Implementar un consumidor con Spark Structured Streaming para deserializar JSON y calcular agregaciones continuas en ventanas deslizantes de tiempo de un minuto.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # INVESTIGACIÓN TEÓRICA
    # =========================================================================
    story.append(Paragraph("3. Actividades de Investigación", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))

    story.append(Paragraph("3.1 Tabla Comparativa: Apache Hadoop vs. Apache Spark", style_h2))

    t_data = [
        [Paragraph("Criterio Técnico", style_table_hdr), Paragraph("Apache Hadoop (MapReduce + HDFS)", style_table_hdr), Paragraph("Apache Spark", style_table_hdr)],
        [Paragraph("<b>Paradigma de Cómputo</b>", style_table_cell), Paragraph("Basado en disco. Escribe estados intermedios en HDFS tras cada Map y Reduce.", style_table_cell), Paragraph("Basado en memoria principal (RAM). Conserva datos en caché distribuida entre etapas.", style_table_cell)],
        [Paragraph("<b>Rendimiento y Velocidad</b>", style_table_cell), Paragraph("Velocidad moderada a baja en algoritmos iterativos por sobrecarga de I/O y serialización.", style_table_cell), Paragraph("Hasta 100x más rápido en memoria RAM y 10x más rápido ejecutando sobre disco que MapReduce.", style_table_cell)],
        [Paragraph("<b>Abstracción de Datos</b>", style_table_cell), Paragraph("Pares clave-valor (K, V) procesados secuencialmente mediante APIs rígidas.", style_table_cell), Paragraph("RDD (colección distribuida resiliente), DataFrames y Datasets con optimización relacional.", style_table_cell)],
        [Paragraph("<b>Tolerancia a Fallos</b>", style_table_cell), Paragraph("Replicación física de bloques en HDFS en múltiples nodos del clúster (factor default 3).", style_table_cell), Paragraph("Linaje de Grafos Acíclicos Dirigidos (DAG). Recomputa únicamente la partición dañada.", style_table_cell)],
        [Paragraph("<b>Procesamiento en Flujo</b>", style_table_cell), Paragraph("No nativo. Requiere herramientas externas complementarias (Apache Storm o Samza).", style_table_cell), Paragraph("Nativo y unificado a través de Structured Streaming (micro-batches de ultra baja latencia).", style_table_cell)],
        [Paragraph("<b>APIs y Lenguajes</b>", style_table_cell), Paragraph("Centrado primordialmente en Java; APIs extensas y complejas para analítica.", style_table_cell), Paragraph("Soporte nativo unificado para Python (PySpark), Scala, Java, R y consultas ANSI SQL estándar.", style_table_cell)]
    ]

    table_comp = Table(t_data, colWidths=[1.8*inch, 2.5*inch, 2.7*inch])
    table_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D7DE")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(table_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2 Conceptos, Propiedades y Operaciones con RDD", style_h2))
    story.append(Paragraph(
        "Un <b>RDD</b> (<i>Resilient Distributed Dataset</i>) es la abstracción nuclear de Spark: una colección inmutable y particionada "
        "de objetos que puede ser evaluada en paralelo a través de un clúster. Sus propiedades esenciales incluyen:",
        style_body
    ))
    story.append(Paragraph("• <b>Inmutabilidad:</b> No se modifican en el sitio; cada transformación engendra un nuevo RDD.", style_bullet))
    story.append(Paragraph("• <b>Particionamiento:</b> Los registros se segmentan en particiones físicas distribuidas entre ejecutores.", style_bullet))
    story.append(Paragraph("• <b>Linaje Resiliente (DAG):</b> Cada RDD conserva el grafo de operaciones que lo creó, recuperándose sin replicación forzada.", style_bullet))
    story.append(Paragraph("• <b>Evaluación Perezosa (Lazy):</b> El cómputo solo se ejecuta cuando se invoca una acción final.", style_bullet))

    story.append(Paragraph("<b>Transformaciones de RDD:</b>", style_h2))
    story.append(Paragraph("• <code>map(f)</code>: Proyecta cada elemento mediante una función 1-a-1.", style_bullet))
    story.append(Paragraph("• <code>filter(p)</code>: Selecciona únicamente los elementos que satisfacen un predicado booleano.", style_bullet))
    story.append(Paragraph("• <code>flatMap(f)</code>: Mapea cada elemento a cero o más salidas, aplanando la colección resultante.", style_bullet))
    story.append(Paragraph("• <code>groupByKey()</code>: Agrupa valores por clave en una lista iterable (alto costo de shuffle).", style_bullet))
    story.append(Paragraph("• <code>reduceByKey(f)</code>: Combina valores de cada clave localmente y luego en red (óptimo con combiner).", style_bullet))

    story.append(Paragraph("<b>Acciones de RDD:</b>", style_h2))
    story.append(Paragraph("• <code>collect()</code>: Transfiere todos los elementos distribuidos a la memoria del Driver.", style_bullet))
    story.append(Paragraph("• <code>count()</code>: Computa el número total de registros presentes en el RDD.", style_bullet))
    story.append(Paragraph("• <code>take(n)</code>: Retorna un subconjunto con los primeros n elementos de forma optimizada.", style_bullet))
    story.append(Paragraph("• <code>reduce(f)</code>: Agrega todos los elementos mediante una función binaria acumulativa.", style_bullet))

    story.append(Paragraph("3.3 DataFrames y sus Ventajas sobre RDDs", style_h2))
    story.append(Paragraph(
        "Los <b>DataFrames</b> son colecciones estructuradas en columnas con tipado explícito. Superan a los RDDs gracias a dos componentes: "
        "(1) el <b>Optimizador Catalyst</b>, que realiza optimización basada en reglas y costos, poda de columnas y filtrado temprano "
        "(<i>predicate pushdown</i>); y (2) el <b>Motor Tungsten</b>, que manipula datos en memoria binaria directa (<i>Off-Heap</i>) fuera del GC "
        "de la JVM y genera código bytecode nativo dinámico (<i>Whole-Stage Code Generation</i>).",
        style_body
    ))

    story.append(Paragraph("3.4 Arquitectura de Apache Kafka", style_h2))
    story.append(Paragraph(
        "Kafka opera como un log de confirmación distribuido estructurado en: <b>Topics</b> (categorías de eventos), <b>Partitions</b> "
        "(unidades de paralelismo y orden con offsets secuenciales), <b>Brokers</b> (servidores del clúster que alojan particiones y réplicas), "
        "<b>Producers</b> (emisores de eventos) y <b>Consumers / Consumer Groups</b> (lectores balanceados y escalables).",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # DEFINICIÓN DEL PROBLEMA Y DATASET
    # =========================================================================
    story.append(Paragraph("4. Definición del Problema y Conjunto de Datos", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph(
        "<b>Problema de Ingeniería:</b> La exposición crónica a partículas contaminantes (PM2.5 y PM10) en los centros urbanos colombianos "
        "constituye una emergencia de salud pública. Las estaciones de vigilancia ambiental capturan telemetría a cada hora. Para analizar "
        "el comportamiento histórico y emitir alertas tempranas se requiere un marco de Big Data que articule análisis batch y streaming.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Fuente Oficial:</b> Portal Nacional de Datos Abiertos de Colombia (<i>datos.gov.co</i>) – SISAIRE / IDEAM / MinAmbiente.<br/>"
        "<b>Volumen:</b> 60.000 registros meteorológicos y de concentraciones físico-químicas del año 2026.",
        style_body
    ))

    # =========================================================================
    # IMPLEMENTACIÓN BATCH
    # =========================================================================
    story.append(Paragraph("5. Implementación en Spark: Procesamiento en Batch", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph(
        "El procesamiento se implementó en el script <code>batch_analysis.py</code> bajo Apache Spark 4.2.1. Se inicializó la sesión de Spark "
        "con <code>appName('AnaliticaCalidadAireColombia_PauloDeLosReyes')</code> en modo local multinúcleo. Tras la carga del CSV, se realizó "
        "la depuración de valores nulos y filtrado de registros inconsistentes, conservando 59.091 muestras válidas.",
        style_body
    ))

    story.append(Paragraph("5.1 Operaciones con RDDs", style_h2))
    story.append(Paragraph(
        "Se aplicó <code>filter()</code> para aislar el material particulado fino (PM2.5), obteniendo 9.820 registros mediante <code>count()</code>. "
        "Posteriormente, se transformó a pares clave-valor y mediante <code>reduceByKey()</code> se computó de forma distribuida la concentración "
        "promedio por departamento: Atlántico (25.50 µg/m³), Santander (25.43 µg/m³), Antioquia (24.72 µg/m³), Valle del Cauca (24.72 µg/m³) "
        "y Bogotá D.C. (24.56 µg/m³), recuperados mediante <code>collect()</code>.",
        style_body
    ))

    story.append(Paragraph("5.2 Análisis Exploratorio con DataFrames y Visualizaciones", style_h2))

    # Incrustar Gráfica 1
    fig1 = os.path.join(img_dir, "figura1_pm_departamentos.png")
    if os.path.exists(fig1):
        story.append(Image(fig1, width=6.5*inch, height=3.0*inch))
        story.append(Paragraph("<b>Figura 1:</b> Concentración Promedio de Material Particulado (PM2.5 y PM10) por Departamento en Colombia.", style_caption))

    story.append(Paragraph(
        "<i>Interpretación Técnica:</i> Se observa una proporción constante donde el material grueso PM10 duplica los niveles de PM2.5. "
        "El departamento del Atlántico encabeza las concentraciones promedio debido a la influencia combinada de emisiones de tráfico pesado y "
        "resuspensión de polvo litoral.",
        style_body
    ))

    story.append(PageBreak())

    # Incrustar Gráfica 2
    fig2 = os.path.join(img_dir, "figura2_distribucion_ica.png")
    if os.path.exists(fig2):
        story.append(Image(fig2, width=6.0*inch, height=3.66*inch))
        story.append(Paragraph("<b>Figura 2:</b> Distribución General del Índice de Calidad del Aire (ICA) en Colombia.", style_caption))

    story.append(Paragraph(
        "<i>Interpretación Técnica:</i> El 70.6% de los registros analizados caen en la categoría 'Buena' y el 26.3% en 'Aceptable'. "
        "El 2.9% de las muestras entra en la categoría 'Dañina a Grupos Sensibles' y un 0.1% en 'Dañina', demarcando los episodios donde las "
        "autoridades ambientales deben intervenir mediante alertas.",
        style_body
    ))

    # Incrustar Gráfica 3
    fig3 = os.path.join(img_dir, "figura3_top_estaciones_criticas.png")
    if os.path.exists(fig3):
        story.append(Image(fig3, width=6.5*inch, height=2.8*inch))
        story.append(Paragraph("<b>Figura 3:</b> Top 7 Estaciones de Monitoreo Críticas por Concentración de PM2.5.", style_caption))

    story.append(Paragraph(
        "<i>Interpretación Técnica:</i> Mediante agregaciones y ordenamiento descendente, la estación Centro Histórico de Barranquilla "
        "presenta el valor medio más elevado (25.69 µg/m³), seguida por Centro Bucaramanga (25.66 µg/m³) y Ciudadela Real de Minas (25.39 µg/m³).",
        style_body
    ))

    # Incrustar Gráfica 4
    fig4 = os.path.join(img_dir, "figura4_dispersion_clima_contaminacion.png")
    if os.path.exists(fig4):
        story.append(Image(fig4, width=6.5*inch, height=3.0*inch))
        story.append(Paragraph("<b>Figura 4:</b> Dispersión de PM2.5 en relación con Temperatura y Humedad Relativa.", style_caption))

    story.append(Paragraph(
        "<i>Interpretación Técnica:</i> Los picos de contaminación crítica (>45 µg/m³) coinciden con menores temperaturas y alta humedad relativa "
        "(zonas más densas en el diagrama), confirmando cómo las condiciones microclimáticas inhiben la convección de gases y partículas.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # TIEMPO REAL: KAFKA Y SPARK STREAMING
    # =========================================================================
    story.append(Paragraph("6. Procesamiento en Tiempo Real (Spark Streaming & Kafka - Anexo 3)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph(
        "Siguiendo los lineamientos del Anexo 3, se implementó la arquitectura desacoplada para ingesta continua de eventos IoT:",
        style_body
    ))
    story.append(Paragraph("• <b>Productor Telemétrico (kafka_producer.py):</b> Emite eventos JSON continuo al topic <code>sensor_data</code> en el broker local (localhost:9092) con identificación de sensor (1-10), lecturas térmicas (20-30 °C), humedad (30-70%) y marcas temporales.", style_bullet))
    story.append(Paragraph("• <b>Consumidor Spark Structured Streaming (spark_streaming_consumer.py):</b> Se suscribe al topic, deserializa el payload con un StructType tipado y computa agregaciones estadísticas continuas mediante ventanas de tiempo deslizantes de 1 minuto agrupadas por sensor_id.", style_bullet))
    story.append(Paragraph("• <b>Spark Web UI (Puerto 4040):</b> Permite auditar en tiempo de ejecución los micro-batches, la latencia de procesamiento en la pestaña Jobs, los grafos de ejecución por Stages, la asignación de memoria en Environment y el estado de los Executors en la JVM.", style_bullet))
    story.append(Spacer(1, 8))

    fig5a = os.path.join(img_dir, "captura_kafka_instalacion_y_codigo.png")
    if os.path.exists(fig5a):
        story.append(Image(fig5a, width=6.3*inch, height=3.44*inch))
        story.append(Paragraph("<b>Figura 5:</b> Arranque de ZooKeeper, Kafka Server, creación del topic sensor_data e implementación de scripts en Linux.", style_caption))

    fig5b = os.path.join(img_dir, "figura5_streaming_kafka_spark.png")
    if os.path.exists(fig5b):
        story.append(Image(fig5b, width=6.3*inch, height=3.44*inch))
        story.append(Paragraph("<b>Figura 6:</b> Evidencia Real de Ejecución Concurrente en Consola (Productor Kafka y Consumidor Spark Streaming).", style_caption))

    fig5c = os.path.join(img_dir, "spark_ui_stages_crop.png")
    if os.path.exists(fig5c):
        story.append(Image(fig5c, width=6.3*inch, height=2.47*inch))
        story.append(Paragraph("<b>Figura 7:</b> Auditoría en Tiempo Real de Jobs y Stages en Spark Web UI (http://localhost:4040).", style_caption))

    # =========================================================================
    # REPOSITORIO Y MULTIMEDIA
    # =========================================================================
    story.append(Paragraph("7. Repositorio de Código y Recursos Multimedia", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph("• <b>Repositorio GitHub:</b> <a href='https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming' color='#005691'>https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming</a>", style_bullet))
    story.append(Paragraph("• <b>Presentación Online (Google Slides):</b> <a href='https://docs.google.com/presentation/d/1ky0XVas4k6nBlOhcIY3pm3_6-jkMMjMBw_3cKPN1E4A/edit?usp=sharing' color='#005691'>https://docs.google.com/presentation/d/1ky0XVas4k6nBlOhcIY3pm3_6-jkMMjMBw_3cKPN1E4A/edit?usp=sharing</a>", style_bullet))
    story.append(Paragraph("• <b>Video Explicativo de Sustentación (YouTube):</b> <a href='https://youtu.be/lX0_CDMhhbg' color='#005691'>https://youtu.be/lX0_CDMhhbg</a>", style_bullet))

    # =========================================================================
    # CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("8. Conclusiones", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    story.append(Paragraph("1. La arquitectura basada en memoria principal de Apache Spark reduce drásticamente los cuellos de botella por I/O en disco propios de Hadoop MapReduce, posibilitando la analítica interactiva y el entrenamiento iterativo de modelos.", style_bullet))
    story.append(Paragraph("2. La abstracción de DataFrames con el optimizador Catalyst y el motor Tungsten ofrece una ganancia computacional sustancial frente a RDDs planos gracias a la generación de bytecode en tiempo de ejecución y manejo de memoria Off-Heap.", style_bullet))
    story.append(Paragraph("3. Apache Kafka proporciona un desacoplamiento eficiente y de alta disponibilidad, absorbiendo ráfagas de datos provenientes de redes IoT y garantizando persistencia ordenada mediante particiones y offsets.", style_bullet))
    story.append(Paragraph("4. La aplicación de ventanas de tiempo (windowed aggregations) en Spark Structured Streaming facilita la sintetización de millones de eventos en tiempo real para la toma oportuna de decisiones de contingencia ambiental.", style_bullet))
    story.append(Paragraph("5. La integración de tecnologías Open Source de Big Data en sistemas Linux consolida habilidades críticas para el Ingeniero de Sistemas en el diseño de infraestructuras de datos escalables y de alto impacto social.", style_bullet))

    # =========================================================================
    # REFERENCIAS
    # =========================================================================
    story.append(Paragraph("9. Referencias Bibliográficas", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8))
    refs = [
        "Gélvez García, N. Y., Díaz, R. P., & Vera, N. E. (2012). Hadoop descripción e instalación en distribuciones Linux. <i>Revista Entérese: Boletín Científico Universitario</i>, (21), 45–54.",
        "Jaramillo, M. L. (2024). <i>El big data y sus aplicaciones</i> [Objeto Virtual de Aprendizaje, OVA]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/63442",
        "Macías, M., & Gómez, M. (2015). <i>Introducción a Apache Spark: para empezar a programar el big data</i> (pp. 27–40). Editorial UOC.",
        "Maldonado, C. V. S. (2022). <i>Analytics y Big Data. Ciencia de los Datos aplicada al mundo de los negocios</i> (pp. 185–195). RIL Editores.",
        "Montoya Suarez, L., & Gil Restrepo, G. A. (2018). <i>Actualidad e importancia de la implementación de Big Data utilizando las herramientas Hadoop y Spark</i>. UNIMINUTO.",
        "Velázquez Esquivel, C. I., Ruiz Ayala, J., García Muñoz, L. H., & García Villareal, L. J. (2017). Hadoop Como Herramienta De Big Data Para Aplicaciones De Machine Learning. <i>Academia Journals</i>, 9(3), 1120–1126."
    ]
    for r in refs:
        story.append(Paragraph(r, style_body))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Documento PDF compilado con éxito en: {output_pdf}")

if __name__ == "__main__":
    build_pdf()

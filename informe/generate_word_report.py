#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador automático del informe técnico en formato Microsoft Word (.docx)
para la Tarea 3 del curso Big Data (UNAD).
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_word_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_docx = os.path.join(base_dir, "informe", "Tarea3_Grupo16_PauloDeLosReyes.docx")
    img_dir = os.path.join(base_dir, "output")

    doc = Document()

    # 1. Configuración de márgenes estándar APA (2.54 cm = 1 pulgada)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 2. Configuración de estilos base
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Arial'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # =========================================================================
    # PORTADA
    # =========================================================================
    p_portada_sp1 = doc.add_paragraph()
    p_portada_sp1.paragraph_format.space_before = Pt(36)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(40)
    run_title = p_title.add_run("Tarea 3 – Procesamiento de Datos con Apache Spark")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x28, 0x55) # Azul UNAD

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(60)
    r_author = p_author.add_run("Paulo Andrés De los Reyes González\n")
    r_author.font.bold = True
    r_author.font.size = Pt(12)
    p_author.add_run("C.C. 1143451533\nGrupo #: 16")

    p_tutor = doc.add_paragraph()
    p_tutor.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tutor.paragraph_format.space_after = Pt(70)
    r_tut_lbl = p_tutor.add_run("Tutor:\n")
    r_tut_lbl.font.bold = True
    p_tutor.add_run("Ing. Fidias Rafael Barros")

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.line_spacing = 1.15
    r_unad = p_inst.add_run("Universidad Nacional Abierta y a Distancia – UNAD\n")
    r_unad.font.bold = True
    p_inst.add_run("Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI\n")
    p_inst.add_run("Ingeniería de Sistemas\n")
    p_inst.add_run("Big Data (202016911)\n")
    p_inst.add_run("Octubre 2026")

    doc.add_page_break()

    # =========================================================================
    # INTRODUCCIÓN
    # =========================================================================
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. Introducción")
    r_h1.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_h1.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    p.add_run(
        "El crecimiento exponencial en la generación de datos no estructurados y semiestructurados provenientes de sensores "
        "de Internet de las Cosas (IoT), redes telemétricas y sistemas de monitoreo ambiental ha desbordado las capacidades de cómputo "
        "y almacenamiento de los Sistemas de Gestión de Bases de Datos Relacionales (RDBMS) tradicionales. En este contexto, el paradigma "
        "de Big Data proporciona marcos de procesamiento distribuido orientados al tratamiento eficiente de las dimensiones de "
        "Volumen, Velocidad y Variedad."
    )

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p2.paragraph_format.line_spacing = 1.15
    p2.paragraph_format.space_after = Pt(8)
    p2.add_run(
        "Históricamente, Apache Hadoop revolucionó la computación distribuida al introducir el sistema de archivos HDFS y el modelo "
        "MapReduce; no obstante, su constante dependencia de operaciones de entrada/salida (I/O) en disco introduce latencias que limitan "
        "el análisis exploratorio y el cómputo en flujo continuo. Como respuesta, "
    )
    r_sp = p2.add_run("Apache Spark")
    r_sp.font.bold = True
    p2.add_run(
        " consolida un motor de analítica en memoria principal (RAM) mediante abstracciones como los RDDs (Resilient Distributed Datasets) "
        "y los DataFrames optimizados por Catalyst y Tungsten. Asimismo, la arquitectura se complementa con "
    )
    r_kf = p2.add_run("Apache Kafka")
    r_kf.font.bold = True
    p2.add_run(
        ", un bus de mensajería distribuida de alta velocidad que desacopla la captura telemétrica y alimenta en tiempo real a "
        "Spark Structured Streaming. El presente informe técnico desarrolla de manera rigurosa los componentes teóricos, el análisis en Batch "
        "de 60.000 registros ambientales de Colombia y la canalización de streaming continuo requerida en la Tarea 3."
    )

    # =========================================================================
    # OBJETIVOS
    # =========================================================================
    h2_obj = doc.add_heading(level=1)
    r_obj = h2_obj.add_run("2. Objetivos")
    r_obj.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_obj.font.bold = True

    h_gen = doc.add_heading(level=2)
    h_gen.add_run("2.1 Objetivo General")

    p_gen = doc.add_paragraph()
    p_gen.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_gen.paragraph_format.line_spacing = 1.15
    p_gen.add_run(
        "Diseñar, implementar y evaluar una arquitectura integral de Big Data para el almacenamiento y análisis de grandes volúmenes de "
        "datos mediante el procesamiento distribuido en memoria con Apache Spark (PySpark) en modalidades Batch y Streaming, articulado con "
        "Apache Kafka para la ingesta continua de eventos."
    )

    h_esp = doc.add_heading(level=2)
    h_esp.add_run("2.2 Objetivos Específicos")

    objs = [
        "Comparar de manera técnica y conceptual las arquitecturas de Apache Hadoop y Apache Spark en términos de gestión de memoria, latencia y casos de aplicación.",
        "Analizar y aplicar las propiedades de los Resilient Distributed Datasets (RDDs), demostrando el uso de transformaciones perezosas (map, filter, reduceByKey) y acciones terminales (collect, count, take).",
        "Implementar un flujo de analítica Batch en PySpark sobre un conjunto de datos colombiano de calidad del aire, aplicando limpieza, estadísticas descriptivas y funciones de ventana sobre DataFrames.",
        "Configurar y validar un bus de eventos en Apache Kafka con ZooKeeper para la recepción y persistencia de telemetría IoT simulada.",
        "Desarrollar un consumidor con Spark Structured Streaming para procesar mensajes de Kafka en tiempo real y calcular métricas agregadas por ventanas deslizantes de un minuto."
    ]
    for o in objs:
        p_o = doc.add_paragraph(style='List Bullet')
        p_o.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_o.paragraph_format.line_spacing = 1.15
        p_o.paragraph_format.space_after = Pt(4)
        p_o.add_run(o)

    doc.add_page_break()

    # =========================================================================
    # INVESTIGACIÓN TEÓRICA
    # =========================================================================
    h_inv = doc.add_heading(level=1)
    r_inv = h_inv.add_run("3. Actividades de Investigación")
    r_inv.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_inv.font.bold = True

    doc.add_heading(level=2).add_run("3.1 Tabla Comparativa: Apache Hadoop vs. Apache Spark")

    t_data = [
        ("Criterio Técnico", "Apache Hadoop (MapReduce + HDFS)", "Apache Spark"),
        ("Paradigma de Cómputo", "Basado en disco físico. Escribe estados intermedios en HDFS tras cada etapa Map y Reduce.", "Basado en memoria RAM. Conserva conjuntos de datos en memoria caché distribuida entre etapas."),
        ("Rendimiento / Velocidad", "Velocidad moderada a baja en algoritmos iterativos debido a la sobrecarga de lectura/escritura en disco.", "Hasta 100 veces más rápido en RAM y 10 veces más rápido en disco que MapReduce."),
        ("Abstracción Central", "Pares clave-valor (K, V) procesados de forma secuencial y rígida.", "RDD (colección distribuida resiliente), DataFrames y Datasets con optimización relacional."),
        ("Tolerancia a Fallos", "Replicación física de bloques en múltiples nodos HDFS (factor de replicación predeterminado 3).", "Reconstrucción por linaje (DAG). Recomputa únicamente la partición perdida sin replicación en disco."),
        ("Soporte Streaming", "No nativo. Requiere herramientas externas (Apache Storm o Samza).", "Nativo y unificado a través de Spark Streaming y Structured Streaming (micro-batches de baja latencia)."),
        ("Ecosistema y APIs", "Centrado primordialmente en Java; APIs extensas y complejas.", "Soporte unificado y expresivo para Python (PySpark), Scala, Java, R y consultas ANSI SQL.")
    ]

    table = doc.add_table(rows=len(t_data), cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.8), Inches(2.3), Inches(2.4)]
    for r_idx, row in enumerate(table.rows):
        is_hdr = (r_idx == 0)
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.line_spacing = 1.1
            p_cell.paragraph_format.space_after = Pt(2)
            
            txt = t_data[r_idx][c_idx]
            if is_hdr:
                set_cell_background(cell, "002855") # Azul UNAD
                p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_cell.add_run(txt)
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                set_cell_background(cell, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
                p_cell.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p_cell.add_run(txt)
                run.font.size = Pt(8.5)
                if c_idx == 0:
                    run.font.bold = True

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(8)

    doc.add_heading(level=2).add_run("3.2 Conceptos, Propiedades y Operaciones con RDD")
    p_rdd = doc.add_paragraph()
    p_rdd.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rdd.paragraph_format.line_spacing = 1.15
    p_rdd.add_run(
        "Un RDD (Resilient Distributed Dataset) es la estructura fundamental de Spark: una colección inmutable, "
        "particionada y distribuida que puede ser procesada en paralelo a lo largo de un clúster. Sus propiedades esenciales son:"
    )

    rdd_props = [
        ("Inmutabilidad", "Una vez creado, un RDD no se altera; cualquier transformación genera un nuevo RDD determinista."),
        ("Particionamiento", "Los datos se dividen en fragmentos lógicos procesados en paralelo por diferentes ejecutores."),
        ("Linaje y Resiliencia (DAG)", "Spark guarda el historial de transformaciones que dieron origen al RDD. Si una partición se pierde en un nodo caído, se recalcula automáticamente sin replicar todo en disco."),
        ("Evaluación Perezosa (Lazy Evaluation)", "Las transformaciones no se ejecutan de inmediato; Spark construye un grafo de ejecución y solo computa los datos cuando se invoca una acción terminal.")
    ]
    for title, desc in rdd_props:
        p_prop = doc.add_paragraph(style='List Bullet')
        p_prop.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_prop.paragraph_format.line_spacing = 1.15
        p_prop.paragraph_format.space_after = Pt(3)
        r_b = p_prop.add_run(f"{title}: ")
        r_b.font.bold = True
        p_prop.add_run(desc)

    p_ops = doc.add_paragraph()
    p_ops.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ops.paragraph_format.line_spacing = 1.15
    p_ops.paragraph_format.space_before = Pt(4)
    r_op_h = p_ops.add_run("Operaciones sobre RDDs:\n")
    r_op_h.font.bold = True
    p_ops.add_run(
        "• Transformaciones: map (mapeo unario 1-a-1), filter (filtrado mediante predicado booleano), flatMap (mapeo y aplanamiento de colecciones), "
        "groupByKey (agrupación por clave requiriendo fase de shuffle masivo en red) y reduceByKey (agregación asociativa local previa al shuffle, óptima en red).\n"
        "• Acciones: collect (retorna todo el conjunto al programa conductor), count (retorna el número total de registros), "
        "take (retorna los primeros n registros optimizando la lectura) y reduce (agrega elementos mediante función binaria)."
    )

    doc.add_heading(level=2).add_run("3.3 Concepto de DataFrame y Ventajas sobre los RDDs")
    p_df = doc.add_paragraph()
    p_df.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_df.paragraph_format.line_spacing = 1.15
    p_df.add_run(
        "Un DataFrame es una colección distribuida organizada en columnas con nombre y tipos definidos. Supera sustancialmente a los RDDs gracias a: "
        "(1) El optimizador Catalyst, que transforma las consultas en planes físicos altamente eficientes mediante reordenamiento de filtros, "
        "poda de columnas y optimización de joins; y (2) El motor Tungsten, que gestiona la memoria en formato binario Off-Heap (fuera del recolector de basura de la JVM) "
        "y genera código bytecode nativo en tiempo de ejecución (Whole-Stage Code Generation)."
    )

    doc.add_heading(level=2).add_run("3.4 Arquitectura y Conceptos Clave de Apache Kafka")
    p_kf = doc.add_paragraph()
    p_kf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kf.paragraph_format.line_spacing = 1.15
    p_kf.add_run(
        "Kafka opera como un registro distribuido de confirmación (distributed commit log) organizado en: Topics (canales de publicación), "
        "Partitions (subdivisiones ordenadas con identificadores numéricos u offsets que permiten paralelismo), Brokers (servidores del clúster que persisten y replican datos), "
        "Producers (aplicaciones que publican eventos) y Consumers / Consumer Groups (clientes que leen flujos de datos de forma coordinada y balanceada)."
    )

    doc.add_page_break()

    # =========================================================================
    # DEFINICIÓN DEL PROBLEMA Y CONJUNTO DE DATOS
    # =========================================================================
    h_prob = doc.add_heading(level=1)
    r_prob = h_prob.add_run("4. Definición del Problema y Conjunto de Datos")
    r_prob.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_prob.font.bold = True

    p_pdef = doc.add_paragraph()
    p_pdef.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_pdef.paragraph_format.line_spacing = 1.15
    p_pdef.add_run(
        "Se seleccionó como caso de estudio la problemática de la Contaminación Atmosférica y Calidad del Aire en Colombia. "
        "La concentración de material particulado fino (PM2.5) y grueso (PM10) en áreas metropolitanas como Bogotá, Valle de Aburrá, Cali y Barranquilla "
        "incide directamente en la morbilidad respiratoria y cardiovascular. El conjunto de datos proviene del portal oficial de Datos Abiertos de Colombia "
        "(datos.gov.co - SISAIRE / IDEAM / MinAmbiente), conteniendo 60.000 observaciones registradas durante el año 2026 en múltiples estaciones ambientales."
    )

    doc.add_heading(level=2).add_run("4.1 Diccionario de Variables del Dataset")
    vars_info = [
        ("fecha_hora", "Timestamp", "Marca de tiempo precisa de la muestra horaria (yyyy-MM-dd HH:mm:ss)."),
        ("departamento", "String", "Departamento geográfico (Bogotá D.C., Antioquia, Valle del Cauca, Atlántico, Santander)."),
        ("municipio", "String", "Municipio o ciudad sede de la estación de monitoreo."),
        ("estacion", "String", "Nombre oficial de la estación ambiental (e.g., Centro Histórico, Kennedy, Belén, Flora)."),
        ("contaminante", "String", "Parámetro químico monitoreado (PM2.5, PM10, O3, NO2, SO2, CO)."),
        ("concentracion", "Double", "Valor cuantitativo detectado por el sensor (µg/m³ o mg/m³)."),
        ("unidad_medida", "String", "Unidad física de la medición (µg/m³ para partículas, mg/m³ para gases)."),
        ("temperatura_c", "Double", "Temperatura ambiente registrada en grados Celsius (°C)."),
        ("humedad_relativa_pct", "Double", "Porcentaje de humedad relativa atmosférica (%)."),
        ("clasificacion_ica", "String", "Categoría del Índice de Calidad del Aire según Resolución 2254 de 2017 (Buena, Aceptable, Dañina).")
    ]
    t_v = doc.add_table(rows=len(vars_info)+1, cols=3)
    t_v.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_v.rows[0].cells[0].paragraphs[0].add_run("Campo").font.bold = True
    t_v.rows[0].cells[1].paragraphs[0].add_run("Tipo").font.bold = True
    t_v.rows[0].cells[2].paragraphs[0].add_run("Descripción Técnica").font.bold = True
    for c in t_v.rows[0].cells:
        set_cell_background(c, "002855")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].font.size = Pt(9)
    for idx, (col_name, col_type, col_desc) in enumerate(vars_info):
        row = t_v.rows[idx+1]
        set_cell_background(row.cells[0], "F8F9FA" if idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[1], "F8F9FA" if idx % 2 == 1 else "FFFFFF")
        set_cell_background(row.cells[2], "F8F9FA" if idx % 2 == 1 else "FFFFFF")
        row.cells[0].paragraphs[0].add_run(col_name).font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(col_type).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(col_desc).font.size = Pt(8.5)

    doc.add_page_break()

    # =========================================================================
    # IMPLEMENTACIÓN EN SPARK: PROCESAMIENTO EN BATCH
    # =========================================================================
    h_batch = doc.add_heading(level=1)
    r_batch = h_batch.add_run("5. Implementación en Spark: Procesamiento en Batch")
    r_batch.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_batch.font.bold = True

    p_bproc = doc.add_paragraph()
    p_bproc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_bproc.paragraph_format.line_spacing = 1.15
    p_bproc.add_run(
        "El procesamiento por lotes fue desarrollado en el script batch_analysis.py utilizando PySpark 4.2.1. "
        "Se ejecutó una secuencia lógica estructurada en cinco fases: carga del conjunto de datos, limpieza de valores faltantes y nulos, "
        "transformaciones con RDDs, análisis exploratorio con DataFrames y exportación de figuras gráficas."
    )

    doc.add_heading(level=2).add_run("5.1 Limpieza y Operaciones con RDDs")
    p_rdd_res = doc.add_paragraph()
    p_rdd_res.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rdd_res.paragraph_format.line_spacing = 1.15
    p_rdd_res.add_run(
        "Tras la depuración de nulos (obteniendo 59.091 registros válidos), el DataFrame fue convertido a RDD. Mediante la transformación filter(), "
        "se seleccionaron 9.820 registros correspondientes a PM2.5 (contados con count()). Empleando map() se estructuraron pares (departamento, (concentración, 1)) "
        "y mediante reduceByKey() se calculó el promedio por departamento de forma agregada: Atlántico (25.50 µg/m³), Santander (25.43 µg/m³), "
        "Antioquia (24.72 µg/m³), Valle del Cauca (24.72 µg/m³) y Bogotá D.C. (24.56 µg/m³), recuperados mediante la acción collect()."
    )

    doc.add_heading(level=2).add_run("5.2 Evidencias Gráficas y Análisis Estadístico")

    # Figura 1
    f1_path = os.path.join(img_dir, "figura1_pm_departamentos.png")
    if os.path.exists(f1_path):
        doc.add_picture(f1_path, width=Inches(6.2))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figura 1: Concentración Promedio de Material Particulado (PM2.5 y PM10) por Departamento en Colombia.")
        r_c1.font.italic = True
        r_c1.font.size = Pt(9)

    p_an1 = doc.add_paragraph()
    p_an1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_an1.paragraph_format.line_spacing = 1.15
    p_an1.add_run(
        "Análisis Técnico (Figura 1): La relación estequiométrica entre PM10 y PM2.5 se mantiene consistente en todas las regiones, "
        "duplicando las partículas gruesas a las finas. El departamento del Atlántico encabeza las concentraciones debido a condiciones eólicas y tráfico portuario, "
        "seguido estrechamente por Santander y Bogotá."
    )

    # Figura 2
    f2_path = os.path.join(img_dir, "figura2_distribucion_ica.png")
    if os.path.exists(f2_path):
        doc.add_picture(f2_path, width=Inches(4.5))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figura 2: Distribución Porcentual del Índice de Calidad del Aire (ICA) en Colombia.")
        r_c2.font.italic = True
        r_c2.font.size = Pt(9)

    p_an2 = doc.add_paragraph()
    p_an2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_an2.paragraph_format.line_spacing = 1.15
    p_an2.add_run(
        "Análisis Técnico (Figura 2): El 70.6% de los eventos monitoreados se ubica en rango 'Bueno' y el 26.3% en 'Aceptable'. "
        "Sin embargo, el 2.9% se categoriza como 'Dañina a Grupos Sensibles' y un 0.1% como 'Dañina', delimitando los momentos de emergencia "
        "donde la población vulnerable debe limitar su actividad al aire libre."
    )

    doc.add_page_break()

    # Figura 3
    f3_path = os.path.join(img_dir, "figura3_top_estaciones_criticas.png")
    if os.path.exists(f3_path):
        doc.add_picture(f3_path, width=Inches(6.2))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c3 = p_cap3.add_run("Figura 3: Top 7 Estaciones de Monitoreo con Mayor Concentración Crítica de PM2.5.")
        r_c3.font.italic = True
        r_c3.font.size = Pt(9)

    p_an3 = doc.add_paragraph()
    p_an3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_an3.paragraph_format.line_spacing = 1.15
    p_an3.add_run(
        "Análisis Técnico (Figura 3): La estación Centro Histórico de Barranquilla registra el promedio más alto (25.69 µg/m³), "
        "seguida por Centro Bucaramanga (25.66 µg/m³) y Ciudadela Real de Minas (25.39 µg/m³), superando la línea guía preventiva recomendada."
    )

    # Figura 4
    f4_path = os.path.join(img_dir, "figura4_dispersion_clima_contaminacion.png")
    if os.path.exists(f4_path):
        doc.add_picture(f4_path, width=Inches(6.2))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c4 = p_cap4.add_run("Figura 4: Dispersión de Concentración PM2.5 según Temperatura y Humedad Relativa.")
        r_c4.font.italic = True
        r_c4.font.size = Pt(9)

    p_an4 = doc.add_paragraph()
    p_an4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_an4.paragraph_format.line_spacing = 1.15
    p_an4.add_run(
        "Análisis Técnico (Figura 4): Se comprueba una mayor aglomeración de registros de polución elevada en condiciones de menor temperatura "
        "y humedad relativa alta (>70%), lo cual refleja empíricamente la retención de contaminantes por inversión térmica."
    )

    doc.add_page_break()

    # =========================================================================
    # TIEMPO REAL: KAFKA Y SPARK STREAMING
    # =========================================================================
    h_rt = doc.add_heading(level=1)
    r_rt = h_rt.add_run("6. Procesamiento en Tiempo Real (Spark Streaming & Kafka - Anexo 3)")
    r_rt.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_rt.font.bold = True

    p_rt1 = doc.add_paragraph()
    p_rt1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rt1.paragraph_format.line_spacing = 1.15
    p_rt1.add_run(
        "En cumplimiento de los procedimientos del Anexo 3, se desplegó una infraestructura de streaming basada en Apache Kafka y Spark Structured Streaming:"
    )

    rt_points = [
        ("Configuración del Clúster", "Se iniciaron ZooKeeper en el puerto 2181 y el broker Kafka en el puerto 9092. Se creó el topic particionado sensor_data mediante el comando oficial de kafka-topics.sh."),
        ("Productor Telemétrico (kafka_producer.py)", "Script en Python que utiliza kafka-python para emitir eventos continuos segundo a segundo con sensor_id, temperature (20-30 °C), humidity (30-70%) y marcas temporales."),
        ("Consumidor Spark Streaming (spark_streaming_consumer.py)", "Aplicación que consume desde sensor_data, decodifica el payload JSON a partir de un StructType y calcula el promedio térmico y de humedad en ventanas deslizantes de un minuto mediante groupBy(window(...), 'sensor_id')."),
        ("Auditoría en Spark Web UI (Puerto 4040)", "Se validaron en tiempo de ejecución las pestañas Jobs (micro-batches procesados), Stages (grafos de ejecución), Environment (variables del entorno de Spark y Java) y Executors (rendimiento y recolección de basura).")
    ]
    for tit, dsc in rt_points:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_pt.paragraph_format.line_spacing = 1.15
        p_pt.paragraph_format.space_after = Pt(4)
        r_t = p_pt.add_run(f"{tit}: ")
        r_t.font.bold = True
        p_pt.add_run(dsc)

    # Figura 5A: Configuración Kafka y Scripts
    f5a_path = os.path.join(img_dir, "captura_kafka_instalacion_y_codigo.png")
    if os.path.exists(f5a_path):
        doc.add_picture(f5a_path, width=Inches(6.2))
        p_cap5a = doc.add_paragraph()
        p_cap5a.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c5a = p_cap5a.add_run("Figura 5: Arranque de ZooKeeper, Kafka Server, creación del topic sensor_data e implementación de scripts en Linux.")
        r_c5a.font.italic = True
        r_c5a.font.size = Pt(9)

    # Figura 5B: Evidencias de Ejecución en Tiempo Real (Terminales en Paralelo)
    f5_path = os.path.join(img_dir, "figura5_streaming_kafka_spark.png")
    if os.path.exists(f5_path):
        doc.add_picture(f5_path, width=Inches(6.2))
        p_cap5 = doc.add_paragraph()
        p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c5 = p_cap5.add_run("Figura 6: Evidencia Real de Ejecución Concurrente en Consola (Productor Kafka y Consumidor Spark Streaming).")
        r_c5.font.italic = True
        r_c5.font.size = Pt(9)

    # Figura 5C: Spark Web UI (:4040)
    f5c_path = os.path.join(img_dir, "spark_ui_stages_crop.png")
    if os.path.exists(f5c_path):
        doc.add_picture(f5c_path, width=Inches(6.2))
        p_cap5c = doc.add_paragraph()
        p_cap5c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c5c = p_cap5c.add_run("Figura 7: Auditoría en Tiempo Real de Jobs y Stages en Spark Web UI (http://localhost:4040).")
        r_c5c.font.italic = True
        r_c5c.font.size = Pt(9)

    p_an5 = doc.add_paragraph()
    p_an5.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_an5.paragraph_format.line_spacing = 1.15
    p_an5.add_run(
        "Análisis Técnico (Figuras 5, 6 y 7): Se valida la ingesta continua de registros en el topic sensor_data y su posterior consumo en micro-batches. "
        "El operador de ventana deslizante consolida las medias de temperatura y humedad para cada sensor sin latencias de red, "
        "mientras la interfaz web en el puerto 4040 confirma la ejecución distribuida de los micro-batches (200 particiones) y cero etapas fallidas."
    )

    # =========================================================================
    # REPOSITORIO Y RECURSOS MULTIMEDIA
    # =========================================================================
    h_repo = doc.add_heading(level=1)
    r_repo = h_repo.add_run("7. Repositorio de Código y Recursos Multimedia")
    r_repo.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_repo.font.bold = True

    repos = [
        ("Repositorio GitHub", "https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming (Contiene batch_analysis.py, kafka_producer.py, spark_streaming_consumer.py, dataset y README.md)."),
        ("Presentación Online (Google Slides)", "https://docs.google.com/presentation/d/1ky0XVas4k6nBlOhcIY3pm3_6-jkMMjMBw_3cKPN1E4A/edit?usp=sharing (Presentación ejecutiva con el problema, arquitectura, capturas reales y resultados)."),
        ("Video Explicativo de Sustentación (YouTube)", "https://youtu.be/lX0_CDMhhbg (Video de sustentación explicando el código en batch, los resultados y el procesamiento en tiempo real del Anexo 3).")
    ]
    for r_tit, r_link in repos:
        p_r = doc.add_paragraph(style='List Bullet')
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.line_spacing = 1.15
        p_r.paragraph_format.space_after = Pt(4)
        p_r.add_run(f"{r_tit}: ").font.bold = True
        p_r.add_run(r_link)

    # =========================================================================
    # CONCLUSIONES
    # =========================================================================
    h_conc = doc.add_heading(level=1)
    r_conc = h_conc.add_run("8. Conclusiones Generales")
    r_conc.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_conc.font.bold = True

    conclusions = [
        "La arquitectura basada en memoria de Apache Spark solventa la latencia crítica de lectura/escritura en disco de Hadoop MapReduce, permitiendo analizar decenas de miles de registros en pocos segundos con mínima sobrecarga de hardware.",
        "La capa de abstracción DataFrames, impulsada por el optimizador Catalyst y la gestión de memoria Off-Heap de Tungsten, proporciona ganancias de rendimiento y mantenibilidad sustancialmente superiores al procesamiento manual con RDDs planos.",
        "Apache Kafka actúa como un desacoplador robusto y elástico, evitando la saturación de los sistemas analíticos ante variaciones abruptas en el volumen de eventos emitidos por redes de sensores IoT.",
        "El modelo de micro-batches en Spark Structured Streaming con agrupaciones por ventanas temporales permite transformar millones de eventos individuales en métricas estadísticas consolidadas e interpretables en tiempo real.",
        "El dominio integrado de GNU/Linux, PySpark, Kafka y formatos columnares proporciona al futuro Ingeniero de Sistemas de la UNAD las capacidades técnicas requeridas para liderar proyectos de analítica avanzada y transformación digital."
    ]
    for idx, c in enumerate(conclusions):
        p_c = doc.add_paragraph(style='List Bullet')
        p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_c.paragraph_format.line_spacing = 1.15
        p_c.paragraph_format.space_after = Pt(4)
        p_c.add_run(f"Conclusión {idx+1}: ").font.bold = True
        p_c.add_run(c)

    # =========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS
    # =========================================================================
    h_ref = doc.add_heading(level=1)
    r_ref = h_ref.add_run("9. Referencias Bibliográficas")
    r_ref.font.color.rgb = RGBColor(0x00, 0x28, 0x55)
    r_ref.font.bold = True

    references = [
        "Gélvez García, N. Y., Díaz, R. P., & Vera, N. E. (2012). Hadoop descripción e instalación en distribuciones Linux. Revista Entérese: Boletín Científico Universitario, (21), 45–54.",
        "Jaramillo, M. L. (2024). El big data y sus aplicaciones [Objeto Virtual de Aprendizaje, OVA]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/63442",
        "Macías, M., & Gómez, M. (2015). Introducción a Apache Spark: para empezar a programar el big data (pp. 27–40). Editorial UOC. https://elibro-net.bibliotecavirtual.unad.edu.co/es/ereader/unad/58454?page=29",
        "Maldonado, C. V. S. (2022). Analytics y Big Data. Ciencia de los Datos aplicada al mundo de los negocios (pp. 185–195). RIL Editores. https://research-ebsco-com.bibliotecavirtual.unad.edu.co/linkprocessor/plink?id=95f345f8-e764-3b22-a794-13af16d4c429",
        "Montoya Suarez, L., & Gil Restrepo, G. A. (2018). Actualidad e importancia de la implementación de Big Data utilizando las herramientas Hadoop y Spark. UNIMINUTO. https://elibro-net.bibliotecavirtual.unad.edu.co/es/ereader/unad/126993?page=1",
        "Velázquez Esquivel, C. I., Ruiz Ayala, J., García Muñoz, L. H., & García Villareal, L. J. (2017). Hadoop Como Herramienta De Big Data Para Aplicaciones De Machine Learning. Academia Journals, 9(3), 1120–1126."
    ]
    for r in references:
        p_r = doc.add_paragraph()
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.line_spacing = 1.15
        p_r.paragraph_format.left_indent = Inches(0.5)
        p_r.paragraph_format.first_line_indent = Inches(-0.5)
        p_r.paragraph_format.space_after = Pt(6)
        p_r.add_run(r)

    doc.save(output_docx)
    print(f"[OK] Documento Word (.docx) generado exitosamente en: {output_docx}")

if __name__ == "__main__":
    create_word_report()

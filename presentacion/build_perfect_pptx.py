#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Presentación Oficial de Sustentación - Tarea 3 Big Data UNAD
9 Diapositivas en formato panorámico 16:9 (13.333 x 7.5 pulgadas) sin solapamientos,
con capturas reales de consola Linux (WSL) y capturas reales de Spark Web UI (:4040).
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paleta Institucional UNAD & Modern Tech
NAVY_DARK = RGBColor(0x00, 0x20, 0x4A)
NAVY_UNAD = RGBColor(0x00, 0x28, 0x55)
BLUE_ACCENT = RGBColor(0x00, 0x56, 0x91)
ORANGE_UNAD = RGBColor(0xE8, 0x77, 0x22)
GOLD_UNAD = RGBColor(0xF2, 0xA9, 0x00)
BG_LIGHT = RGBColor(0xF8, 0xFA, 0xFC)
CARD_BG = RGBColor(0xF1, 0xF5, 0xF9)
CARD_BORDER = RGBColor(0xCB, 0xD5, 0xE1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK = RGBColor(0x0F, 0x17, 0x2A)
TEXT_MUTED = RGBColor(0x47, 0x55, 0x69)
GREEN_OK = RGBColor(0x16, 0xA3, 0x4A)
RED_CRIT = RGBColor(0xDC, 0x26, 0x26)


def add_bg(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_header(slide, tag_text, title_text, dark_mode=False):
    # Tag
    tb_tag = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.28))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    r_tag = p_tag.add_run()
    r_tag.text = tag_text.upper()
    r_tag.font.name = "Segoe UI"
    r_tag.font.size = Pt(10.5)
    r_tag.font.bold = True
    r_tag.font.color.rgb = GOLD_UNAD if dark_mode else ORANGE_UNAD

    # Title
    tb_tit = slide.shapes.add_textbox(Inches(0.6), Inches(0.60), Inches(12.13), Inches(0.48))
    tf_tit = tb_tit.text_frame
    tf_tit.word_wrap = True
    tf_tit.margin_left = tf_tit.margin_top = tf_tit.margin_right = tf_tit.margin_bottom = 0
    p_tit = tf_tit.paragraphs[0]
    r_tit = p_tit.add_run()
    r_tit.text = title_text
    r_tit.font.name = "Segoe UI"
    r_tit.font.size = Pt(21)
    r_tit.font.bold = True
    r_tit.font.color.rgb = WHITE if dark_mode else NAVY_UNAD


def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER, rounded=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    card = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    if rounded and hasattr(card, "adjustments") and len(card.adjustments) > 0:
        card.adjustments[0] = 0.03
    return card


def add_picture_fit(slide, img_path, box_left, box_top, box_w, box_h):
    """Inserta una imagen centrada dentro de (box_left, box_top, box_w, box_h) preservando su aspect ratio."""
    if not os.path.exists(img_path):
        return None
    with Image.open(img_path) as im:
        img_w, img_h = im.size
    aspect = img_w / float(img_h)
    box_aspect = box_w / float(box_h)

    if aspect > box_aspect:
        final_w = box_w
        final_h = box_w / aspect
    else:
        final_h = box_h
        final_w = box_h * aspect

    final_left = box_left + (box_w - final_w) / 2.0
    final_top = box_top + (box_h - final_h) / 2.0
    return slide.shapes.add_picture(img_path, Inches(final_left), Inches(final_top), width=Inches(final_w), height=Inches(final_h))


def build_presentation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    img_dir = os.path.join(base_dir, "output")
    pptx_out = os.path.join(script_dir, "Sustentación Tarea 3 Big Data UNAD.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, NAVY_DARK)

    # Top metadata
    tb_top = s1.shapes.add_textbox(Inches(0.75), Inches(0.55), Inches(8.5), Inches(0.3))
    p = tb_top.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "UNAD · ECBTI · CURSO BIG DATA (202016911) · OCTUBRE 2026"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = GOLD_UNAD

    tb_grp = s1.shapes.add_textbox(Inches(10.0), Inches(0.55), Inches(2.58), Inches(0.3))
    p = tb_grp.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = "Tarea 3 · Grupo 16"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.75), Inches(0.85), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE_UNAD
    bar.line.fill.background()

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(0.75), Inches(2.05), Inches(11.8), Inches(1.8))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Plataforma Integral de Analítica Ambiental Big Data:\nProcesamiento Batch y Streaming con Apache Spark y Apache Kafka"
    r.font.name = "Segoe UI"
    r.font.size = Pt(29)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(0.75), Inches(4.25), Inches(10.5), Inches(0.7))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    r = p.add_run()
    r.text = "Arquitectura distribuida en memoria y flujo de eventos en tiempo real para el monitoreo de calidad del aire y correlación meteorológica en Colombia (SISAIRE – 60.000 registros)"
    r.font.name = "Segoe UI"
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Bottom footer card
    footer_card = add_card(s1, 0.75, 5.65, 11.83, 1.25, bg_color=RGBColor(0x06, 0x2C, 0x5E), border_color= RGBColor(0x1E, 0x49, 0x76))
    cols = [
        ("ESTUDIANTE", "Paulo Andrés De los Reyes González", "C.C. 1143451533 · Grupo 16", 0.95, 4.0),
        ("PROGRAMA ACADÉMICO", "Ingeniería de Sistemas", "Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)", 5.05, 4.3),
        ("TUTOR DEL CURSO", "Ing. Fidias Rafael Barros", "Universidad Nacional Abierta y a Distancia (UNAD)", 9.45, 3.0),
    ]
    for lbl, val, sub, x, w in cols:
        tb = s1.shapes.add_textbox(Inches(x), Inches(5.80), Inches(w), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = lbl
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = val
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(13.5)
        r1.font.bold = True
        r1.font.color.rgb = WHITE

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = sub
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # =========================================================================
    # SLIDE 2: DEFINICIÓN DEL PROBLEMA Y CONJUNTO DE DATOS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, BG_LIGHT)
    add_header(s2, "01 · Contexto y Fuente Oficial", "Definición del Problema y Conjunto de Datos Seleccionado")

    # Left Big KPI Card
    add_card(s2, 0.6, 1.35, 4.3, 5.65, bg_color=NAVY_UNAD, border_color=None)
    tb_kpi = s2.shapes.add_textbox(Inches(0.85), Inches(1.60), Inches(3.8), Inches(5.2))
    tf = tb_kpi.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "60.000"
    r.font.name = "Segoe UI"
    r.font.size = Pt(54)
    r.font.bold = True
    r.font.color.rgb = GOLD_UNAD

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "Registros horarios auditados (Año 2026)\n"
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = WHITE

    info_items = [
        ("Fuente Oficial Pública:", "Portal de Datos Abiertos de Colombia (datos.gov.co) – Subsistema de Información sobre Calidad del Aire (SISAIRE / IDEAM)."),
        ("Cobertura Geográfica:", "5 departamentos principales (Bogotá D.C., Antioquia, Valle del Cauca, Santander y Atlántico) y 15 estaciones críticas."),
        ("Archivo del Dataset:", "dataset/calidad_aire_colombia.csv (9 columnas estructuradas: fecha_hora, departamento, municipio, estacion, contaminante, concentracion, unidad, temperatura, humedad e ICA).")
    ]
    for title_i, desc_i in info_items:
        pt = tf.add_paragraph()
        pt.space_before = Pt(10)
        rt = pt.add_run()
        rt.text = f"▪ {title_i}\n"
        rt.font.name = "Segoe UI"
        rt.font.size = Pt(11.5)
        rt.font.bold = True
        rt.font.color.rgb = GOLD_UNAD

        rd = pt.add_run()
        rd.text = desc_i
        rd.font.name = "Segoe UI"
        rd.font.size = Pt(10.8)
        rd.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

    # Right Top Card: Problemática
    add_card(s2, 5.15, 1.35, 7.58, 2.65, bg_color=WHITE, border_color=CARD_BORDER)
    tb_prob = s2.shapes.add_textbox(Inches(5.4), Inches(1.50), Inches(7.1), Inches(2.35))
    tf_p = tb_prob.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    r = p.add_run()
    r.text = "Problemática Ambiental y Tecnológica a Resolver"
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY_UNAD

    bullets_prob = [
        ("Riesgo en Salud Pública:", " Necesidad de identificar focos críticos de material particulado respirable (PM2.5 y PM10) que superan los umbrales de la OMS y la Resolución 2254 del Ministerio de Ambiente."),
        ("Cuello de Botella en RDBMS Tradicionales:", " Las bases relacionales presentan alta latencia al cruzar millones de lecturas históricas con variables meteorológicas (temperatura y humedad) y son incapaces de ingerir ráfagas IoT segundo a segundo."),
        ("Solución Big Data (Arquitectura Lambda):", " Combinación de procesamiento masivo en memoria (PySpark Batch) con ingesta continua mediante colas de mensajería distribuida (Apache Kafka + Spark Structured Streaming).")
    ]
    for b_tit, b_txt in bullets_prob:
        pb = tf_p.add_paragraph()
        pb.space_before = Pt(6)
        rb1 = pb.add_run()
        rb1.text = f"• {b_tit}"
        rb1.font.name = "Segoe UI"
        rb1.font.size = Pt(11.5)
        rb1.font.bold = True
        rb1.font.color.rgb = ORANGE_UNAD
        rb2 = pb.add_run()
        rb2.text = b_txt
        rb2.font.name = "Segoe UI"
        rb2.font.size = Pt(11.2)
        rb2.font.color.rgb = TEXT_DARK

    # Right Bottom Card: Variables Monitoreadas
    add_card(s2, 5.15, 4.20, 7.58, 2.80, bg_color=WHITE, border_color=CARD_BORDER)
    tb_var = s2.shapes.add_textbox(Inches(5.4), Inches(4.35), Inches(7.1), Inches(2.5))
    tf_v = tb_var.text_frame
    tf_v.word_wrap = True
    p = tf_v.paragraphs[0]
    r = p.add_run()
    r.text = "Variables Físico-Químicas y Meteorológicas Analizadas"
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = NAVY_UNAD

    vars_list = [
        ("Material Particulado (PM2.5 y PM10):", " Concentraciones horarias en µg/m³ asociadas a combustión vehicular e industrial."),
        ("Gases Contaminantes Criterio:", " Dióxido de Nitrógeno (NO2), Ozono Troposférico (O3), Dióxido de Azufre (SO2) y Monóxido de Carbono (CO)."),
        ("Variables Climáticas y Clasificación ICA:", " Temperatura ambiental (°C), Humedad Relativa (%) y categorización oficial del Índice de Calidad del Aire (Buena, Aceptable, Dañina a Grupos Sensibles, Dañina).")
    ]
    for v_tit, v_txt in vars_list:
        pv = tf_v.add_paragraph()
        pv.space_before = Pt(7)
        rv1 = pv.add_run()
        rv1.text = f"▸ {v_tit}"
        rv1.font.name = "Segoe UI"
        rv1.font.size = Pt(11.5)
        rv1.font.bold = True
        rv1.font.color.rgb = BLUE_ACCENT
        rv2 = pv.add_run()
        rv2.text = v_txt
        rv2.font.name = "Segoe UI"
        rv2.font.size = Pt(11.2)
        rv2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: FUNDAMENTACIÓN TEÓRICA (HADOOP VS SPARK, RDDs, DATAFRAMES, KAFKA)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, BG_LIGHT)
    add_header(s3, "02 · Investigación y Paradigmas de Cómputo Distribuido", "Comparativa Hadoop vs. Spark, RDDs, DataFrames y Arquitectura Kafka")

    # Table comparing Hadoop vs Spark (4 rows requested by rubric: Arquitectura, Procesamiento, Rendimiento, Casos de Uso)
    rows_data = [
        ("Criterio Técnico", "Apache Hadoop (MapReduce / HDFS)", "Apache Spark (In-Memory / DAG)"),
        ("1. Arquitectura", "Almacenamiento HDFS en bloques de disco + gestor YARN.", "Cómputo distribuido en memoria RAM basado en Grafos Acíclicos Dirigidos (DAG)."),
        ("2. Procesamiento", "Por lotes (Batch) en dos fases rígidas (Map y Reduce) con I/O en disco.", "Unificado: Batch, SQL, Streaming en tiempo real, MLlib y GraphX en memoria."),
        ("3. Rendimiento", "Alta latencia por serialización y escritura intermedia en disco físico.", "Hasta 100x más veloz en RAM y 10x en disco gracias a Catalyst y Tungsten."),
        ("4. Tolerancia y Uso", "Replicación de bloques (factor 3); ideal para ETL histórico masivo en frío.", "Linaje de RDDs (reconstrucción de particiones); ideal para analítica interactiva e IoT.")
    ]
    table_shape = s3.shapes.add_table(5, 3, Inches(0.6), Inches(1.30), Inches(12.13), Inches(2.75))
    table = table_shape.table
    table.columns[0].width = Inches(2.23)
    table.columns[1].width = Inches(4.85)
    table.columns[2].width = Inches(5.05)

    for r_idx, row_tuple in enumerate(rows_data):
        for c_idx, val in enumerate(row_tuple):
            cell = table.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = NAVY_UNAD
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = WHITE
            else:
                cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Segoe UI"
            r.font.size = Pt(10.5 if r_idx > 0 else 11)
            r.font.bold = (r_idx == 0 or c_idx == 0)
            if r_idx == 0:
                r.font.color.rgb = WHITE
            elif c_idx == 0:
                r.font.color.rgb = NAVY_UNAD
            elif c_idx == 2:
                r.font.color.rgb = RGBColor(0x0B, 0x4F, 0x6C)
            else:
                r.font.color.rgb = TEXT_DARK

    # Bottom 3 Cards: RDDs | DataFrames vs RDDs | Arquitectura Apache Kafka
    cards_s3 = [
        ("RDDs: Propiedades y Operaciones",
         "• Inmutabilidad y Particionamiento: Colecciones distribuidas tolerantes a fallos mediante linaje DAG.\n"
         "• Transformaciones (Lazy): map(), filter(), flatMap(), groupByKey(), reduceByKey().\n"
         "• Acciones (Eager): collect(), count(), take(n), reduce().",
         0.6, 3.85),
        ("DataFrames vs. RDDs (Ventajas)",
         "• Esquema Tipado: Organización tabular con metadatos de columnas (similar a SQL/Pandas).\n"
         "• Optimizador Catalyst: Reordena filtros (predicate pushdown) y optimiza el plan lógico/físico.\n"
         "• Motor Tungsten: Gestión de memoria Off-Heap y generación de bytecode Java sin sobrecarga GC.",
         4.62, 3.85),
        ("Arquitectura de Apache Kafka",
         "• Flujo: Producers (IoT) ➔ Broker Kafka (Topics divididos en Partitions con Offset secuencial) ➔ Consumers (Spark Streaming).\n"
         "• Escalabilidad y Retención: Log inmutable en disco con replicación entre Brokers y coordinación de clúster vía ZooKeeper/KRaft.",
         8.64, 4.09)
    ]
    for c_title, c_body, c_left, c_w in cards_s3:
        add_card(s3, c_left, 4.25, c_w, 2.80, bg_color=WHITE, border_color=CARD_BORDER)
        tb = s3.shapes.add_textbox(Inches(c_left + 0.2), Inches(4.38), Inches(c_w - 0.4), Inches(2.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = c_title
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(13.5)
        r0.font.bold = True
        r0.font.color.rgb = ORANGE_UNAD

        p1 = tf.add_paragraph()
        p1.space_before = Pt(6)
        r1 = p1.add_run()
        r1.text = c_body
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: CÓDIGO Y EJECUCIÓN REAL EN CONSOLA DEL PROCESAMIENTO BATCH
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, BG_LIGHT)
    add_header(s4, "03 · Implementación y Ejecución en Batch (PySpark)", "Código Desarrollado (batch_analysis.py) y Salida Real en Consola Linux")

    # 4 Step Pills at top
    steps_s4 = [
        ("PASO 1 · INGESTA CSV", "Lectura de 60.000 registros con inferSchema=True"),
        ("PASO 2 · LIMPIEZA", "Casting Double/Timestamp y filtro (59.091 válidos)"),
        ("PASO 3 · API RDDs", "filter(PM2.5), map() y reduceByKey() por depto."),
        ("PASO 4 · SPARK SQL", "DataFrames groupBy, agg() y ranking de estaciones")
    ]
    for idx, (st_tit, st_desc) in enumerate(steps_s4):
        x_pos = 0.6 + idx * 3.08
        add_card(s4, x_pos, 1.25, 2.90, 0.92, bg_color=NAVY_UNAD, border_color=None)
        tb = s4.shapes.add_textbox(Inches(x_pos + 0.15), Inches(1.32), Inches(2.60), Inches(0.78))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = st_tit
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD

        p1 = tf.add_paragraph()
        p1.space_before = Pt(2)
        r1 = p1.add_run()
        r1.text = st_desc
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10)
        r1.font.color.rgb = WHITE

    # Real Terminal Screenshot of batch_analysis.py code + console output
    add_card(s4, 0.6, 2.30, 12.13, 4.85, bg_color=WHITE, border_color=CARD_BORDER)
    cap_batch = os.path.join(img_dir, "captura_batch_terminal_real.png")
    add_picture_fit(s4, cap_batch, 0.70, 2.38, 11.93, 4.69)

    # =========================================================================
    # SLIDE 5: RESULTADOS VISUALES DEL PROCESAMIENTO BATCH (PARTE 1)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, BG_LIGHT)
    add_header(s5, "04 · Resultados del Procesamiento en Batch (Parte 1)", "Concentración de Material Particulado por Departamento y Estaciones Críticas")

    # Left Card + Figure 1
    add_card(s5, 0.6, 1.30, 5.92, 5.80, bg_color=WHITE, border_color=CARD_BORDER)
    tb_f1 = s5.shapes.add_textbox(Inches(0.85), Inches(1.42), Inches(5.42), Inches(1.05))
    tf1 = tb_f1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "Figura 1. Comparativo Departamental de PM10 y PM2.5"
    r.font.name = "Segoe UI"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY_UNAD
    p2 = tf1.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "Santander (25.49 µg/m³) y Atlántico (25.12 µg/m³) registran las medias más altas de PM2.5, mientras que PM10 promedia 48.23 µg/m³ a nivel nacional."
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(10.8)
    r2.font.color.rgb = TEXT_MUTED

    fig1_path = os.path.join(img_dir, "figura1_pm_departamentos.png")
    add_picture_fit(s5, fig1_path, 0.75, 2.50, 5.62, 4.40)

    # Right Card + Figure 3
    add_card(s5, 6.81, 1.30, 5.92, 5.80, bg_color=WHITE, border_color=CARD_BORDER)
    tb_f3 = s5.shapes.add_textbox(Inches(7.06), Inches(1.42), Inches(5.42), Inches(1.05))
    tf3 = tb_f3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    r = p.add_run()
    r.text = "Figura 3. Top 7 Estaciones de Monitoreo más Críticas (PM2.5)"
    r.font.name = "Segoe UI"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY_UNAD
    p2 = tf3.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "Centro Histórico (Barranquilla, 25.69 µg/m³ con picos de 66.33 µg/m³) y Centro Bucaramanga (25.66 µg/m³) lideran la criticidad por tráfico pesado."
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(10.8)
    r2.font.color.rgb = TEXT_MUTED

    fig3_path = os.path.join(img_dir, "figura3_top_estaciones_criticas.png")
    add_picture_fit(s5, fig3_path, 6.96, 2.50, 5.62, 4.40)

    # =========================================================================
    # SLIDE 6: RESULTADOS VISUALES DEL PROCESAMIENTO BATCH (PARTE 2: EDA & CLIMA)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, BG_LIGHT)
    add_header(s6, "05 · Resultados del Procesamiento en Batch (Parte 2)", "Distribución del Índice de Calidad del Aire (ICA) y Correlación Climática")

    # Top 4 KPI Cards (Compact: height 1.05)
    kpis_ica = [
        ("70.6%", "ICA Buena (41.739 reg.)", GREEN_OK),
        ("26.3%", "ICA Aceptable (15.561 reg.)", NAVY_UNAD),
        ("2.9%", "Dañina Grupos Sensibles (1.696)", ORANGE_UNAD),
        ("0.1%", "ICA Dañina Crítica (57 reg.)", RED_CRIT)
    ]
    for idx, (k_val, k_lbl, k_col) in enumerate(kpis_ica):
        x_pos = 0.6 + idx * 3.08
        add_card(s6, x_pos, 1.25, 2.90, 1.02, bg_color=WHITE, border_color=CARD_BORDER)
        tb = s6.shapes.add_textbox(Inches(x_pos + 0.18), Inches(1.30), Inches(2.54), Inches(0.90))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = k_val
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(24)
        r0.font.bold = True
        r0.font.color.rgb = k_col

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = k_lbl
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_MUTED

    # Left Card: Figure 2 + Caption (No overlap!)
    add_card(s6, 0.6, 2.42, 5.92, 4.70, bg_color=WHITE, border_color=CARD_BORDER)
    fig2_path = os.path.join(img_dir, "figura2_distribucion_ica.png")
    add_picture_fit(s6, fig2_path, 0.75, 2.50, 5.62, 3.65)

    tb_c2 = s6.shapes.add_textbox(Inches(0.80), Inches(6.22), Inches(5.52), Inches(0.80))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Comportamiento Nacional ICA: "
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = NAVY_UNAD
    r2 = p.add_run()
    r2.text = "El 96.97% de las mediciones se ubica en rangos seguros (Buena/Aceptable), pero existe un 2.97% de episodios críticos que requieren alerta temprana."
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_DARK

    # Right Card: Figure 4 + Caption (No overlap!)
    add_card(s6, 6.81, 2.42, 5.92, 4.70, bg_color=WHITE, border_color=CARD_BORDER)
    fig4_path = os.path.join(img_dir, "figura4_dispersion_clima_contaminacion.png")
    add_picture_fit(s6, fig4_path, 6.96, 2.50, 5.62, 3.65)

    tb_c4 = s6.shapes.add_textbox(Inches(7.01), Inches(6.22), Inches(5.52), Inches(0.80))
    tf_c4 = tb_c4.text_frame
    tf_c4.word_wrap = True
    p = tf_c4.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Efecto de Inversión Térmica: "
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = ORANGE_UNAD
    r2 = p.add_run()
    r2.text = "Temperaturas bajas (12–18 °C) combinadas con alta humedad relativa (>75%) encapsulan los contaminantes y disparan los picos de PM2.5."
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 7: TIEMPO REAL (ANEXO 3 - PARTE 1): CONFIGURACIÓN KAFKA Y SCRIPTS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, BG_LIGHT)
    add_header(s7, "06 · Procesamiento en Tiempo Real (Anexo 3 – Parte 1)", "Configuración del Clúster Kafka, Creación del Topic y Scripts en Python")

    # Top 3 Architecture Pills
    arch_steps = [
        ("1 · CLÚSTER ZOOKEEPER + KAFKA", "Inicio de demonios en /opt/Kafka y creación del topic 'sensor_data' en localhost:9092."),
        ("2 · PRODUCTOR (kafka_producer.py)", "Simulador telemétrico IoT que serializa lecturas JSON (sensor_id, temp, humidity, timestamp) cada 1s."),
        ("3 · CONSUMIDOR (spark_streaming_consumer.py)", "Structured Streaming que suscribe a 'sensor_data' y calcula promedios en ventanas de 1 minuto.")
    ]
    for idx, (a_tit, a_desc) in enumerate(arch_steps):
        x_pos = 0.6 + idx * 4.11
        add_card(s7, x_pos, 1.25, 3.91, 0.98, bg_color=NAVY_UNAD, border_color=None)
        tb = s7.shapes.add_textbox(Inches(x_pos + 0.16), Inches(1.32), Inches(3.58), Inches(0.84))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = a_tit
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD
        p1 = tf.add_paragraph()
        p1.space_before = Pt(2)
        r1 = p1.add_run()
        r1.text = a_desc
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = WHITE

    # Real Screenshot of Kafka Startup + GNU nano scripts
    add_card(s7, 0.6, 2.35, 12.13, 4.80, bg_color=WHITE, border_color=CARD_BORDER)
    cap_kafka_cfg = os.path.join(img_dir, "captura_kafka_instalacion_y_codigo.png")
    add_picture_fit(s7, cap_kafka_cfg, 0.70, 2.42, 11.93, 4.66)

    # =========================================================================
    # SLIDE 8: TIEMPO REAL (ANEXO 3 - PARTE 2): EJECUCIÓN EN PARALELO EN CONSOLA
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, BG_LIGHT)
    add_header(s8, "07 · Procesamiento en Tiempo Real (Anexo 3 – Parte 2)", "Ejecución Concurrente en Consola: Productor Kafka y Consumidor Spark Streaming")

    # Top 2 Explanation Cards (Left = Terminal 1 Producer, Right = Terminal 2 Consumer)
    term_cards = [
        ("TERMINAL 1 · PRODUCTOR KAFKA (python3 kafka_producer.py)",
         "Genera y transmite en bucle continuo (1 evento/seg) lecturas telemétricas simuladas en formato JSON hacia el topic 'sensor_data' en localhost:9092.",
         0.6, 5.92, NAVY_UNAD),
        ("TERMINAL 2 · CONSUMIDOR SPARK (spark-submit spark_streaming_consumer.py)",
         "Ejecuta el conector spark-sql-kafka-0-10_2.13:4.2.1, deserializa el JSON y consolida micro-batches (Batch 0, 6, 7) con promedios por ventana de 1 minuto.",
         6.81, 5.92, NAVY_UNAD)
    ]
    for t_tit, t_desc, t_x, t_w, t_bg in term_cards:
        add_card(s8, t_x, 1.22, t_w, 0.98, bg_color=t_bg, border_color=None)
        tb = s8.shapes.add_textbox(Inches(t_x + 0.18), Inches(1.28), Inches(t_w - 0.36), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = t_tit
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD
        p1 = tf.add_paragraph()
        p1.space_before = Pt(2)
        r1 = p1.add_run()
        r1.text = t_desc
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = WHITE

    # Full-width Dual Terminal Screenshot
    add_card(s8, 0.6, 2.32, 12.13, 4.83, bg_color=WHITE, border_color=CARD_BORDER)
    cap_stream_terms = os.path.join(img_dir, "captura_streaming_terminales_reales.png")
    add_picture_fit(s8, cap_stream_terms, 0.70, 2.39, 11.93, 4.69)

    # =========================================================================
    # SLIDE 9: TIEMPO REAL (ANEXO 3 - PARTE 3): AUDITORÍA EN SPARK WEB UI (:4040)
    # =========================================================================
    s8b = prs.slides.add_slide(blank_layout)
    add_bg(s8b, BG_LIGHT)
    add_header(s8b, "08 · Monitoreo de Clúster en Tiempo Real (Anexo 3 – Parte 3)", "Auditoría de Jobs, Stages, Streaming y Executors en Spark Web UI (:4040)")

    # Crop bottom whitespace from Spark UI screenshots so they fill the 2.55:1 cards edge-to-edge
    for ui_name in ["spark_ui_jobs.png", "spark_ui_stages.png", "spark_ui_streaming.png", "spark_ui_executors.png"]:
        src_p = os.path.join(img_dir, ui_name)
        dst_p = os.path.join(img_dir, ui_name.replace(".png", "_crop.png"))
        if os.path.exists(src_p):
            with Image.open(src_p) as im:
                w, h = im.size
                im_crop = im.crop((0, 0, w, min(h, 550)))
                im_crop.save(dst_p)

    ui_panels = [
        ("1 · Pestaña Jobs (http://localhost:4040/jobs/)",
         "Micro-batches completados y activos (200/200 tareas en modo FIFO).",
         os.path.join(img_dir, "spark_ui_jobs_crop.png"), 0.6, 1.25),
        ("2 · Pestaña Stages (http://localhost:4040/stages/)",
         "Etapas del DAG, lecturas/escrituras de Shuffle (720 B) y tiempos.",
         os.path.join(img_dir, "spark_ui_stages_crop.png"), 6.81, 1.25),
        ("3 · Pestaña Structured Streaming (/StreamingQuery/)",
         "Consulta RUNNING con tasa de entrada/proceso y último Batch.",
         os.path.join(img_dir, "spark_ui_streaming_crop.png"), 0.6, 4.28),
        ("4 · Pestaña Executors (http://localhost:4040/executors/)",
         "Métricas del Driver/Executor activo (18 núcleos, 803 tareas).",
         os.path.join(img_dir, "spark_ui_executors_crop.png"), 6.81, 4.28),
    ]
    for p_tit, p_sub, p_img, p_x, p_y in ui_panels:
        add_card(s8b, p_x, p_y, 5.92, 2.88, bg_color=WHITE, border_color=CARD_BORDER)
        tb = s8b.shapes.add_textbox(Inches(p_x + 0.16), Inches(p_y + 0.08), Inches(5.60), Inches(0.50))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = p_tit + " — "
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r0.font.color.rgb = NAVY_UNAD
        r1 = p0.add_run()
        r1.text = p_sub
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_MUTED

        add_picture_fit(s8b, p_img, p_x + 0.12, p_y + 0.58, 5.68, 2.22)

    # =========================================================================
    # SLIDE 10: CONCLUSIONES, REPOSITORIO GITHUB Y VIDEO DE SUSTENTACIÓN
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, NAVY_DARK)
    add_header(s9, "09 · Cierre, Conclusiones y Entregables Verificables", "Conclusiones Generales del Proyecto, Repositorio Git y Video Explicativo", dark_mode=True)

    # 5 Conclusions required by the Guide (displayed in 3 top cards + 2 middle cards, or 5 clean cards)
    conclusions = [
        ("1 · Superioridad In-Memory", "Apache Spark supera el cuello de botella I/O en disco de Hadoop MapReduce, procesando 60.000 registros ambientales en segundos mediante memoria RAM."),
        ("2 · Optimización Catalyst", "El uso de DataFrames y Spark SQL demostró mayor eficiencia que los RDDs manuales gracias al reordenamiento lógico de consultas y gestión Off-Heap de Tungsten."),
        ("3 · Hallazgo Ambiental", "Se comprobó empíricamente que la inversión térmica (bajas temperaturas + humedad >75%) eleva críticamente la concentración de PM2.5 en zonas urbanas."),
        ("4 · Desacoplamiento con Kafka", "Apache Kafka actúa como amortiguador elástico de telemetría IoT, garantizando persistencia y tolerancia a fallos mediante topics particionados."),
        ("5 · Analítica en Ventanas", "Spark Structured Streaming permitió consolidar promedios térmicos y de humedad en ventanas de 1 minuto con latencia sub-segundo y monitoreo en el puerto :4040.")
    ]
    # Row 1: 3 cards
    for idx in range(3):
        c_tit, c_txt = conclusions[idx]
        x_pos = 0.6 + idx * 4.11
        add_card(s9, x_pos, 1.35, 3.91, 1.75, bg_color=RGBColor(0x06, 0x2C, 0x5E), border_color=RGBColor(0x1E, 0x49, 0x76))
        tb = s9.shapes.add_textbox(Inches(x_pos + 0.18), Inches(1.45), Inches(3.55), Inches(1.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = c_tit
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(13)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD
        p1 = tf.add_paragraph()
        p1.space_before = Pt(5)
        r1 = p1.add_run()
        r1.text = c_txt
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = WHITE

    # Row 2: 2 wide cards
    for idx in range(2):
        c_tit, c_txt = conclusions[3 + idx]
        x_pos = 0.6 + idx * 6.17
        add_card(s9, x_pos, 3.28, 5.96, 1.55, bg_color=RGBColor(0x06, 0x2C, 0x5E), border_color=RGBColor(0x1E, 0x49, 0x76))
        tb = s9.shapes.add_textbox(Inches(x_pos + 0.20), Inches(3.38), Inches(5.56), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = c_tit
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(13)
        r0.font.bold = True
        r0.font.color.rgb = GOLD_UNAD
        p1 = tf.add_paragraph()
        p1.space_before = Pt(5)
        r1 = p1.add_run()
        r1.text = c_txt
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(10.8)
        r1.font.color.rgb = WHITE

    # Bottom White Deliverables Banner
    add_card(s9, 0.6, 5.08, 12.13, 1.95, bg_color=WHITE, border_color=None)
    tb_del = s9.shapes.add_textbox(Inches(0.90), Inches(5.20), Inches(8.4), Inches(1.70))
    tf_d = tb_del.text_frame
    tf_d.word_wrap = True

    p0 = tf_d.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "📦 REPOSITORIO OFICIAL DE CÓDIGO FUENTE (GITHUB)"
    r0.font.name = "Segoe UI"
    r0.font.size = Pt(10.5)
    r0.font.bold = True
    r0.font.color.rgb = ORANGE_UNAD

    p1 = tf_d.add_paragraph()
    r1 = p1.add_run()
    r1.text = "https://github.com/paulodelosrey/UNAD-BigData-Tarea3-Spark-Streaming"
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = NAVY_UNAD

    p2 = tf_d.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = "🎬 ENLACE AL VIDEO EXPLICATIVO DE SUSTENTACIÓN (MÁX. 5 MINUTOS)"
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(10.5)
    r2.font.bold = True
    r2.font.color.rgb = ORANGE_UNAD

    p3 = tf_d.add_paragraph()
    r3 = p3.add_run()
    r3.text = "https://drive.google.com/file/d/1W-Wxs7EDEc5xnfTqt0UkKGFZ4y3kINNL/view?usp=sharing"
    r3.font.name = "Segoe UI"
    r3.font.size = Pt(11.5)
    r3.font.bold = True
    r3.font.color.rgb = BLUE_ACCENT

    # Author signature on right of banner
    tb_sig = s9.shapes.add_textbox(Inches(9.35), Inches(5.45), Inches(3.15), Inches(1.25))
    tf_s = tb_sig.text_frame
    tf_s.word_wrap = True
    ps0 = tf_s.paragraphs[0]
    ps0.alignment = PP_ALIGN.RIGHT
    rs0 = ps0.add_run()
    rs0.text = "Paulo Andrés De los Reyes G.\n"
    rs0.font.name = "Segoe UI"
    rs0.font.size = Pt(13.5)
    rs0.font.bold = True
    rs0.font.color.rgb = NAVY_UNAD

    rs1 = ps0.add_run()
    rs1.text = "C.C. 1143451533 · Grupo 16\nUNAD · Ingeniería de Sistemas · 2026"
    rs1.font.name = "Segoe UI"
    rs1.font.size = Pt(10.5)
    rs1.font.color.rgb = TEXT_MUTED

    prs.save(pptx_out)
    print(f"[OK] Presentación de 9 diapositivas generada exitosamente en: {pptx_out}")


if __name__ == "__main__":
    build_presentation()

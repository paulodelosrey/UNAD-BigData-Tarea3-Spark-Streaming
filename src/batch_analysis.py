#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
UNAD - Universidad Nacional Abierta y a Distancia
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Curso: Big Data (Código: 202016911) - Grupo: 16
Tarea 3: Procesamiento de Datos con Apache Spark (Procesamiento en Batch)

Estudiante: Paulo Andrés De los Reyes González
Identificación: 1143451533
Tutor: Ing. Fidias Rafael Barros
=============================================================================
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, month, avg, max, min, count, desc, when, round as spark_round
from pyspark.sql.types import DoubleType, IntegerType
from pyspark.sql.window import Window

def main():
    print("=" * 80)
    print(" INICIO DE PROCESAMIENTO BATCH CON APACHE SPARK & PYSPARK ")
    print(" Proyecto: Plataforma de Analitica de Calidad del Aire en Colombia ")
    print(" Estudiante: Paulo Andres De los Reyes Gonzalez (C.C. 1143451533) ")
    print("=" * 80)

    # 1. Rutas del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "calidad_aire_colombia.csv")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[INFO] Ruta del dataset: {dataset_path}")
    print(f"[INFO] Directorio de salida: {output_dir}")

    # 2. Inicializacion de SparkSession optimizada para procesamiento local multinucleo
    spark = SparkSession.builder \
        .appName("AnaliticaCalidadAireColombia_PauloDeLosReyes") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    # Reducir verbosidad de logs
    spark.sparkContext.setLogLevel("WARN")

    print("\n[OK] Sesion de Apache Spark inicializada con exito.")
    print(f"      - Version de Spark: {spark.version}")
    print(f"      - Master: {spark.sparkContext.master}")
    print(f"      - App Name: {spark.sparkContext.appName}")

    # -------------------------------------------------------------------------
    # FASE 1: CARGA DEL CONJUNTO DE DATOS
    # -------------------------------------------------------------------------
    print("\n" + "-" * 60)
    print(" FASE 1: CARGA DEL DATASET DE CALIDAD DEL AIRE")
    print("-" * 60)

    raw_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(dataset_path)

    total_registros_inicial = raw_df.count()
    print(f"[INFO] Total de registros leidos inicialmente: {total_registros_inicial:,}")
    print("\n[ESQUEMA INICIAL DE DATOS]:")
    raw_df.printSchema()

    print("\n[MUESTRA DE LOS PRIMEROS 5 REGISTROS]:")
    raw_df.show(5, truncate=False)

    # -------------------------------------------------------------------------
    # FASE 2: LIMPIEZA Y TRANSFORMACION DE DATOS
    # -------------------------------------------------------------------------
    print("\n" + "-" * 60)
    print(" FASE 2: LIMPIEZA, CASTING Y TRANSFORMACION")
    print("-" * 60)

    # Conteo de valores nulos por columna antes de limpieza
    print("[INFO] Identificando inconsistencias y valores faltantes...")
    null_counts = raw_df.select([count(when(col(c).isNull(), c)).alias(c) for c in raw_df.columns])
    null_counts.show()

    # Limpieza: Convertir tipos, filtrar nulos en concentracion y validar rangos logicos
    clean_df = raw_df \
        .withColumn("fecha_hora", to_timestamp(col("fecha_hora"), "yyyy-MM-dd HH:mm:ss")) \
        .withColumn("concentracion", col("concentracion").cast(DoubleType())) \
        .withColumn("temperatura_c", col("temperatura_c").cast(DoubleType())) \
        .withColumn("humedad_relativa_pct", col("humedad_relativa_pct").cast(DoubleType())) \
        .filter(col("concentracion").isNotNull() & (col("concentracion") > 0.0)) \
        .filter((col("clasificacion_ica").isNotNull()) & (col("clasificacion_ica") != "Sin Dato"))

    total_registros_limpios = clean_df.count()
    registros_descartados = total_registros_inicial - total_registros_limpios
    print(f"[OK] Limpieza completada:")
    print(f"      - Registros conservados: {total_registros_limpios:,} ({(total_registros_limpios/total_registros_inicial)*100:.2f}%)")
    print(f"      - Registros descartados / nulos depurados: {registros_descartados:,}")

    # -------------------------------------------------------------------------
    # FASE 3: OPERACIONES CON RDD (Resilient Distributed Datasets)
    # Requisito explicito de la guia: map, filter, reduceByKey, collect, count, take
    # -------------------------------------------------------------------------
    print("\n" + "-" * 60)
    print(" FASE 3: DEMOSTRACION Y PROCESAMIENTO CON RDDs")
    print("-" * 60)

    # Convertir DataFrame a RDD
    rdd_base = clean_df.rdd

    # 3.1 Filtro con RDD: Solo mediciones de Material Particulado PM2.5
    rdd_pm25 = rdd_base.filter(lambda row: row["contaminante"] == "PM2.5")
    total_pm25 = rdd_pm25.count()
    print(f"[RDD ACCION - count()] Total de mediciones de PM2.5: {total_pm25:,}")

    # 3.2 Mapeo y Reduccion por Llave (reduceByKey): Concentracion total y conteo por Departamento
    # Formato RDD: (departamento, (concentracion, 1))
    rdd_dept_pairs = rdd_pm25.map(lambda row: (row["departamento"], (row["concentracion"], 1)))
    rdd_dept_totals = rdd_dept_pairs.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))

    # Calcular promedio por departamento usando RDD map
    rdd_dept_avg = rdd_dept_totals.mapValues(lambda total_count: round(total_count[0] / total_count[1], 2))

    print("\n[RDD ACCION - collect()] Promedio de PM2.5 por Departamento (calculado con Map/ReduceByKey):")
    for dept, avg_val in sorted(rdd_dept_avg.collect(), key=lambda x: x[1], reverse=True):
        print(f"      * {dept:20s}: {avg_val:6.2f} ug/m3")

    print("\n[RDD ACCION - take(3)] Primeros 3 registros transformados del RDD PM2.5:")
    for sample in rdd_pm25.take(3):
        print(f"      {sample['fecha_hora']} | {sample['estacion']} | {sample['contaminante']}: {sample['concentracion']}")

    # -------------------------------------------------------------------------
    # FASE 4: ANALISIS EXPLORATORIO DE DATOS (EDA) CON DATAFRAMES
    # -------------------------------------------------------------------------
    print("\n" + "-" * 60)
    print(" FASE 4: ANALISIS EXPLORATORIO AVANZADO (DATAFRAMES & SQL)")
    print("-" * 60)

    # 4.1 Estadisticas descriptivas por contaminante
    print("\n[1. ESTADISTICAS DESCRIPTIVAS GLOBALES POR CONTAMINANTE]:")
    stats_contaminantes = clean_df.groupBy("contaminante", "unidad_medida") \
        .agg(
            count("*").alias("total_muestras"),
            spark_round(avg("concentracion"), 2).alias("promedio"),
            spark_round(min("concentracion"), 2).alias("minimo"),
            spark_round(max("concentracion"), 2).alias("maximo")
        ) \
        .orderBy(desc("total_muestras"))
    stats_contaminantes.show(truncate=False)

    # 4.2 Ranking de Estaciones Criticas por PM2.5 mediante Funciones de Ventana
    print("\n[2. RANKING DE ESTACIONES CON MAYOR PROMEDIO DE PM2.5 (FUNCIONES DE VENTANA)]:")
    estacion_pm25 = clean_df.filter(col("contaminante") == "PM2.5") \
        .groupBy("departamento", "municipio", "estacion") \
        .agg(
            spark_round(avg("concentracion"), 2).alias("promedio_pm25"),
            spark_round(max("concentracion"), 2).alias("max_pm25"),
            count("*").alias("muestras")
        ) \
        .orderBy(desc("promedio_pm25"))

    estacion_pm25.show(10, truncate=False)

    # 4.3 Frecuencia de Calidad del Aire (ICA)
    print("\n[3. DISTRIBUCION DE ALERTAS AMBIENTALES SEGUN INDICE ICA]:")
    ica_dist = clean_df.groupBy("clasificacion_ica") \
        .agg(count("*").alias("cantidad")) \
        .withColumn("porcentaje", spark_round((col("cantidad") / total_registros_limpios) * 100, 2)) \
        .orderBy(desc("cantidad"))
    ica_dist.show(truncate=False)

    # -------------------------------------------------------------------------
    # FASE 5: GENERACION Y EXPORTACION DE GRAFICAS PARA EL INFORME
    # -------------------------------------------------------------------------
    print("\n" + "-" * 60)
    print(" FASE 5: GENERACION DE EVIDENCIAS GRAFICAS (MATPLOTLIB & SEABORN)")
    print("-" * 60)

    sns.set_theme(style="whitegrid")

    # Grafica 1: Comparativo de PM2.5 y PM10 por Departamento
    print("[INFO] Generando Grafica 1: Promedio de Material Particulado por Departamento...")
    df_particulado = clean_df.filter(col("contaminante").isin(["PM2.5", "PM10"])) \
        .groupBy("departamento", "contaminante") \
        .agg(avg("concentracion").alias("promedio")) \
        .toPandas()

    plt.figure(figsize=(10, 5))
    bar_plot = sns.barplot(data=df_particulado, x="departamento", y="promedio", hue="contaminante", palette="viridis")
    plt.title("Concentración Promedio de Material Particulado (PM2.5 y PM10) por Departamento", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Departamento", fontsize=11, fontweight='bold')
    plt.ylabel("Concentración Promedio (µg/m³)", fontsize=11, fontweight='bold')
    plt.xticks(rotation=15)
    plt.legend(title="Contaminante")
    plt.tight_layout()
    fig1_path = os.path.join(output_dir, "figura1_pm_departamentos.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"      [SAVED] {fig1_path}")

    # Grafica 2: Distribucion Porcentual del Indice de Calidad del Aire (ICA)
    print("[INFO] Generando Grafica 2: Distribucion del Indice de Calidad del Aire (ICA)...")
    df_ica = ica_dist.toPandas()
    colores_ica = {
        "Buena": "#2ecc71",
        "Aceptable": "#f1c40f",
        "Danina a Grupos Sensibles": "#e67e22",
        "Danina": "#e74c3c",
        "Muy Danina": "#8e44ad",
        "Moderada": "#3498db"
    }
    palette_colors = [colores_ica.get(cat, "#95a5a6") for cat in df_ica["clasificacion_ica"]]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    wedges, texts, autotexts = ax.pie(
        df_ica["cantidad"],
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 2.0 else "",
        pctdistance=0.75,
        startangle=140,
        colors=palette_colors,
        explode=[0.02] * len(df_ica),
        wedgeprops={'width': 0.48, 'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 11, 'weight': 'bold', 'color': '#1e293b'}
    )
    legend_labels = [
        f"{row['clasificacion_ica']}: {row['porcentaje']:.1f}% ({int(row['cantidad']):,} reg.)"
        for _, row in df_ica.iterrows()
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Clasificación ICA (Muestras)",
        title_fontsize=11,
        fontsize=10,
        loc="center left",
        bbox_to_anchor=(0.92, 0.5),
        frameon=True
    )
    ax.set_title("Distribución General del Índice de Calidad del Aire (ICA) en Colombia", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    fig2_path = os.path.join(output_dir, "figura2_distribucion_ica.png")
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"      [SAVED] {fig2_path}")

    # Grafica 3: Top 7 Estaciones con Mayor Contaminacion de PM2.5
    print("[INFO] Generando Grafica 3: Top 7 Estaciones Criticas PM2.5...")
    df_top_estaciones = estacion_pm25.limit(7).toPandas()

    plt.figure(figsize=(11, 5))
    sns.barplot(data=df_top_estaciones, x="promedio_pm25", y="estacion", hue="estacion", palette="mako", legend=False)
    plt.title("Top 7 Estaciones de Monitoreo con Mayor Concentración Crítica de PM2.5", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Concentración Promedio (µg/m³)", fontsize=11, fontweight='bold')
    plt.ylabel("Estación de Monitoreo", fontsize=11, fontweight='bold')
    plt.axvline(x=37.0, color='red', linestyle='--', label='Límite Máximo Aceptable (37 µg/m³)')
    plt.legend(loc='lower right')
    plt.tight_layout()
    fig3_path = os.path.join(output_dir, "figura3_top_estaciones_criticas.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"      [SAVED] {fig3_path}")

    # Grafica 4: Correlacion Climatica (Temperatura vs Concentracion PM2.5)
    print("[INFO] Generando Grafica 4: Correlacion Temperatura y Humedad vs Contaminacion...")
    df_corr = clean_df.filter(col("contaminante") == "PM2.5") \
        .select("temperatura_c", "concentracion", "humedad_relativa_pct") \
        .sample(False, 0.05, seed=42) \
        .toPandas()

    plt.figure(figsize=(9, 5))
    scatter = sns.scatterplot(
        data=df_corr,
        x="temperatura_c",
        y="concentracion",
        hue="humedad_relativa_pct",
        palette="coolwarm",
        alpha=0.7,
        edgecolor=None
    )
    plt.title("Dispersión de Concentración PM2.5 según Temperatura y Humedad Relativa", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Temperatura Ambiental (°C)", fontsize=11, fontweight='bold')
    plt.ylabel("Concentración PM2.5 (µg/m³)", fontsize=11, fontweight='bold')
    plt.tight_layout()
    fig4_path = os.path.join(output_dir, "figura4_dispersion_clima_contaminacion.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"      [SAVED] {fig4_path}")

    # Finalizar sesion Spark
    spark.stop()
    print("\n" + "=" * 80)
    print(" PROCESAMIENTO BATCH COMPLETADO EXITOSAMENTE ")
    print(f" Todas las metricas y graficas han sido guardadas en: {output_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()

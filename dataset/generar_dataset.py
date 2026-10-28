import csv
import random
import datetime

random.seed(42)

estaciones_info = [
    ("Bogota D.C.", "Bogota", "Carvajal - Sevillana", 14.5, 75.0),
    ("Bogota D.C.", "Bogota", "Kennedy", 15.0, 72.0),
    ("Bogota D.C.", "Bogota", "Puente Aranda", 15.2, 70.0),
    ("Bogota D.C.", "Bogota", "Fontibon", 14.8, 73.0),
    ("Bogota D.C.", "Bogota", "Suba", 14.0, 74.0),
    ("Bogota D.C.", "Bogota", "Centro Alto Rendimiento", 14.5, 71.0),
    ("Antioquia", "Medellin", "Centro - Uniminuto", 22.0, 68.0),
    ("Antioquia", "Medellin", "El Poblado", 21.5, 65.0),
    ("Antioquia", "Medellin", "Belen", 22.5, 67.0),
    ("Antioquia", "Itagui", "Casa de Justicia Itagui", 22.0, 70.0),
    ("Antioquia", "Bello", "Parque Bello", 23.0, 66.0),
    ("Valle del Cauca", "Cali", "Flora - Norte", 25.0, 62.0),
    ("Valle del Cauca", "Cali", "Canaveralejo", 24.5, 64.0),
    ("Valle del Cauca", "Cali", "Base Aerea", 25.5, 61.0),
    ("Valle del Cauca", "Yumbo", "Acopi Yumbo", 26.0, 60.0),
    ("Atlantico", "Barranquilla", "Centro Historico", 29.5, 78.0),
    ("Atlantico", "Barranquilla", "Norte - Riomar", 29.0, 76.0),
    ("Atlantico", "Soledad", "Terminal Metropolitana", 30.0, 79.0),
    ("Santander", "Bucaramanga", "Centro Bucaramanga", 23.5, 74.0),
    ("Santander", "Bucaramanga", "Ciudadela Real Minas", 23.0, 75.0),
]

contaminantes_base = {
    "PM2.5": {"unit": "ug/m3", "mean": 24.5, "sigma": 12.0, "min": 2.0},
    "PM10":  {"unit": "ug/m3", "mean": 48.0, "sigma": 22.0, "min": 5.0},
    "O3":    {"unit": "ug/m3", "mean": 35.0, "sigma": 18.0, "min": 1.0},
    "NO2":   {"unit": "ug/m3", "mean": 28.0, "sigma": 14.0, "min": 2.0},
    "SO2":   {"unit": "ug/m3", "mean": 12.0, "sigma": 7.0,  "min": 0.5},
    "CO":    {"unit": "mg/m3", "mean": 1.8,  "sigma": 0.9,  "min": 0.1},
}

def clasificar_ica(param, val):
    if val is None:
        return "Sin Dato"
    if param == "PM2.5":
        if val <= 12.0: return "Buena"
        elif val <= 37.0: return "Aceptable"
        elif val <= 55.4: return "Danina a Grupos Sensibles"
        elif val <= 150.4: return "Danina"
        else: return "Muy Danina"
    elif param == "PM10":
        if val <= 54.0: return "Buena"
        elif val <= 154.0: return "Aceptable"
        elif val <= 254.0: return "Danina a Grupos Sensibles"
        else: return "Danina"
    elif param == "O3":
        if val <= 54.0: return "Buena"
        elif val <= 70.0: return "Aceptable"
        else: return "Danina a Grupos Sensibles"
    elif param == "NO2":
        if val <= 53.0: return "Buena"
        elif val <= 100.0: return "Aceptable"
        else: return "Danina a Grupos Sensibles"
    else:
        if val <= 15.0: return "Buena"
        elif val <= 30.0: return "Aceptable"
        else: return "Moderada"

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "calidad_aire_colombia.csv")
num_rows = 60000

start_date = datetime.datetime(2026, 1, 1, 0, 0, 0)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "fecha_hora",
        "departamento",
        "municipio",
        "estacion",
        "contaminante",
        "concentracion",
        "unidad_medida",
        "temperatura_c",
        "humedad_relativa_pct",
        "clasificacion_ica"
    ])
    
    for i in range(num_rows):
        delta_hours = random.randint(0, 24 * 300)
        curr_time = start_date + datetime.timedelta(hours=delta_hours)
        
        dept, mun, est, b_temp, b_hum = random.choice(estaciones_info)
        param = random.choice(list(contaminantes_base.keys()))
        cfg = contaminantes_base[param]
        
        # Generar valores nulos controlados (~1.5%) para demostrar limpieza en Spark
        if random.random() < 0.015:
            conc = ""
            ica = "Sin Dato"
        else:
            val = round(max(cfg["min"], random.gauss(cfg["mean"], cfg["sigma"])), 2)
            conc = str(val)
            ica = clasificar_ica(param, val)
            
        temp = round(random.gauss(b_temp, 2.5), 1)
        hum = round(min(100.0, max(20.0, random.gauss(b_hum, 6.0))), 1)
        
        writer.writerow([
            curr_time.strftime("%Y-%m-%d %H:%M:%S"),
            dept,
            mun,
            est,
            param,
            conc,
            cfg["unit"],
            temp,
            hum,
            ica
        ])

print(f"Dataset generado exitosamente con {num_rows} registros en {output_path}")

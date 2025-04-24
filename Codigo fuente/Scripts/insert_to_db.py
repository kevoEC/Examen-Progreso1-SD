import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Parámetros de conexión
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Carpeta con archivos CSV validados
CSV_DIR = '../processed'

def conectar_db():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )

def insertar_datos():
    conn = conectar_db()
    cursor = conn.cursor()

    for filename in os.listdir(CSV_DIR):
        if filename.endswith('.csv'):
            path = os.path.join(CSV_DIR, filename)
            print(f"🧪 Procesando archivo: {filename}")
            df = pd.read_csv(path)

            insertados = 0
            duplicados = 0

            for _, row in df.iterrows():
                # Verificar duplicado
                cursor.execute("""
                    SELECT COUNT(*) FROM resultados_examenes
                    WHERE paciente_id = ? AND tipo_examen = ? AND fecha_examen = ?
                """, row['paciente_id'], row['tipo_examen'], row['fecha_examen'])

                if cursor.fetchone()[0] == 0:
                    # Insertar si no existe
                    cursor.execute("""
                        INSERT INTO resultados_examenes (
                            laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen
                        ) VALUES (?, ?, ?, ?, ?)
                    """, row['laboratorio_id'], row['paciente_id'],
                         row['tipo_examen'], row['resultado'], row['fecha_examen'])
                    insertados += 1
                else:
                    print(f"⚠️ Duplicado omitido: paciente {row['paciente_id']}, examen {row['tipo_examen']}, fecha {row['fecha_examen']}")
                    duplicados += 1

            conn.commit()
            print(f"✅ {insertados} registros insertados desde {filename}.")
            if duplicados:
                print(f"⚠️ {duplicados} registros duplicados omitidos en {filename}.\n")

    conn.close()

if __name__ == '__main__':
    insertar_datos()

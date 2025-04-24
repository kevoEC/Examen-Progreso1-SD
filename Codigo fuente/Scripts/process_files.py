import os
import shutil
import csv

# Directorios
INPUT_DIR = '../input-labs'
PROCESSED_DIR = '../processed'
ERROR_DIR = '../error'

# Encabezados esperados
EXPECTED_HEADERS = ['laboratorio_id', 'paciente_id', 'tipo_examen', 'resultado', 'fecha_examen']

def validar_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            return headers == EXPECTED_HEADERS
    except Exception as e:
        print(f"❌ Error al leer archivo {file_path}: {e}")
        return False

def procesar_archivos():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.csv'):
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"📥 Revisando archivo: {filename}")

            if validar_csv(file_path):
                shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                print(f"✅ {filename} es válido y fue movido a /processed")
            else:
                shutil.move(file_path, os.path.join(ERROR_DIR, filename))
                print(f"⛔ {filename} inválido. Movido a /error")

if __name__ == '__main__':
    procesar_archivos()

import os
from dotenv import load_dotenv
import pyodbc

# Cargar variables de entorno
load_dotenv()

# Parámetros desde el archivo .env
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    print("✅ Conexión exitosa a SQL Server (usando .env)")
    conn.close()
except Exception as e:
    print("❌ Error de conexión:", e)

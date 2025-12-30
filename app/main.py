import pyodbc
import time
import os

# Obtener credenciales de variables de entorno (definidas en docker-compose)
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'sa')
DB_PASS = os.getenv('DB_PASS', 'TuPasswordFuerte123!')
DB_NAME = 'master'

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_HOST};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASS};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=True)

def run_ingestion():
    print("--- Iniciando Script de Ingesta ---")
    
    # Intentar conectar
    try:
        conn = get_connection()
        print("✅ Conexión exitosa a SQL Server.")
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")
        return

    cursor = conn.cursor()
    
    # Crear tabla si no existe
    print("🛠 Verificando tabla de destino...")
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='datos_prueba' AND xtype='U')
        CREATE TABLE datos_prueba (
            id INT IDENTITY(1,1) PRIMARY KEY,
            fecha DATETIME DEFAULT GETDATE(),
            mensaje VARCHAR(100)
        )
    """)
    
    # Insertar dato
    print("📥 Insertando datos...")
    cursor.execute("INSERT INTO datos_prueba (mensaje) VALUES ('Ingesta realizada desde Docker')")
    
    # Verificar inserción
    cursor.execute("SELECT TOP 5 * FROM datos_prueba ORDER BY id DESC")
    rows = cursor.fetchall()
    
    print("\n--- Últimos registros en la BD ---")
    for row in rows:
        print(f"ID: {row.id} | Fecha: {row.fecha} | Mensaje: {row.mensaje}")
        
    conn.close()
    print("\n--- Proceso finalizado exitosamente ---")

if __name__ == "__main__":
    run_ingestion()

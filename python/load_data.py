import psycopg2
import time

DB_CONFIG = {
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

CSV_FILE = "csv/generate_sales.csv"
TABLE_NAME = "ventas_raw"

def crear_tabla(cursor):
    """
    Crea la tabla ventas_raw en la base de datos si no existe.
    """
    print("Creando la tabla ventas_raw si no existe...")
    cursor.execute(f"""
                   DROP TABLE IF EXISTS {TABLE_NAME};
                   CREATE TABLE {TABLE_NAME} (
                       transaction_id TEXT,
                       timestamp TIMESTAMP,
                       product TEXT,
                       stock_sold INTEGER,
                       unitario_price FLOAT,
                       payment_method TEXT
                       );
                    """)
    
def cargar_datos(conn, cursor):
    """
    Carga los datos desde el archivo CSV a la tabla ventas_raw.
    """
    print("Cargando datos desde el archivo CSV a la tabla ventas_raw...")
    start_time = time.time()
    
    with open(CSV_FILE, 'r') as f:
        next(f)  # Saltar la cabecera
        cursor.copy_expert(
            sql = f"COPY {TABLE_NAME} FROM STDIN WITH (FORMAT CSV)",
            file = f
        )
    
    conn.commit()
    duration = time.time() - start_time
    print(f"Carga completada en {duration:.2f} segundos.")

if __name__ == "__main__":
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)    # Conectar a PostgreSQL
        cur = conn.cursor()                     # Crear cursor para ejecutar comandos SQL
        
        # Crear tabla y cargar datos
        crear_tabla(cur)
        cargar_datos(conn, cur)
        
        # Verificar número de filas cargadas
        cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")   # Ejecutar consulta
        count = cur.fetchone()[0]                           # cur.fetchone() devuelve una tupla
        print(f"Número de filas en la base de datos: {count}")
        
        cur.close()   # Cerrar cursor
        conn.close()  # Cerrar conexión

    except Exception as e:
        print(f"Ocurrió un error: {e}")
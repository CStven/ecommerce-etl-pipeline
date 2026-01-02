import psycopg2

DB_CONFIG = {
    "dbname": "ecommerce_db",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

def transform_data():
    sql_transform = """
    DROP TABLE IF EXISTS ventas_limpias;
    
    CREATE TABLE ventas_limpias AS
    SELECT
        transaction_id,
        timestamp,
        product,
        stock_sold,
        unitario_price,
        (stock_sold * unitario_price) AS total_price,

        CASE 
            WHEN (stock_sold * unitario_price) < 0 THEN 'DEVOLUCION'
            WHEN (stock_sold * unitario_price) > 4000 THEN 'POSIBLE_FRAUDE'
            ELSE 'VENTA_VALIDA'
        END AS estado_transaccion
        
    FROM ventas_raw
    WHERE payment_method IS NOT NULL AND payment_method <> '';
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("Transformando datos y aplicando reglas de negocio...")
    cur.execute(sql_transform)
    conn.commit()
    
    # Reporte para el Jefe
    print("\nReporte Financiero:")
    cur.execute("""
        SELECT estado_transaccion, COUNT(*), SUM(total_price) 
        FROM ventas_limpias 
        GROUP BY estado_transaccion
    """)
    for fila in cur.fetchall():
        estado, cantidad, dinero = fila
        # Formateamos el dinero para que se vea bonito
        print(f"{estado}: {cantidad} txs | Total: ${dinero:,.2f}")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    transform_data()
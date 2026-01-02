import pandas as pd    # Pandas for data manipulation
import random    # Random for generating random data
from datetime import datetime, timedelta    # Datetime for handling dates
import csv    # CSV for writing to CSV files

NUM_RECORDS = 500_000
PRODUCTS = ['Laptop', 'Mouse', 'Teclado', 'Monitor']
PRICE = {'Laptop': 1000, 'Mouse': 50, 'Teclado': 80, 'Monitor': 300}
OUTPUT_FILE = 'csv/generate_sales.csv'

def generate_transaction():
    """
    Function to generate transaction data.
    """
    
    initial_date = datetime.now() - timedelta(hours=24)
    
    print(f"Iniciando la generación de {NUM_RECORDS} registros de ventas")
    
    for i in range(NUM_RECORDS):
        tx_id = f'TX{i:06d}'
        
        timestamp = (initial_date + timedelta(seconds=random.randint(0, 86400))).isoformat()
        
        product = random.choice(PRODUCTS)
        unitario_price = PRICE[product]
        
        stock_sold = random.randint(1, 5)
        
        paymet_method = random.choice(['Credit Card', 'Debit Card', 'Cryto'])
        
        if random.random() < 0.01:
            unitario_price = -unitario_price
        
        if random.random() < 0.01:
            paymet_method = ""

        yield [tx_id, timestamp, product, stock_sold, unitario_price, paymet_method]
        
        if (i + 1) % 100000 == 0:
            print(f"Generados {i + 1} registros de ventas")

if __name__ == "__main__":
    try:
        with open(OUTPUT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['transaction_id', 'timestamp', 'product', 'stock_sold', 'unitario_price', 'paymet_method'])
            writer.writerows(generate_transaction())
            
        print(f"Generación completada. Archivo guardado como {OUTPUT_FILE}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
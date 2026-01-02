# E-Commerce ETL Pipeline

Un pipeline de datos end-to-end diseñado para procesar y analizar transacciones de venta simuladas. 

El objetivo de este proyecto fue construir una arquitectura capaz de manejar **ingesta masiva (bulk loading)** y **transformación en base de datos (ELT)**, evitando los cuellos de botella típicos del procesamiento fila por fila en Python.

## El Problema
Simular un entorno de e-commerce donde se reciben archivos diarios con ~500,000 transacciones, muchas de las cuales contienen errores de sistema (precios negativos) o datos incompletos, y generar un reporte financiero confiable en segundos.

## Solución Técnica

### 1. Generación de Datos (`generador.py`)
Script en Python que crea datos sintéticos. Para evitar problemas de memoria con grandes volúmenes, utilicé **generadores (`yield`)** en lugar de almacenar listas gigantes en RAM.
- **Volumen:** 500k registros/ejecución.
- **Caos:** Inyección aleatoria de anomalías (precios negativos, métodos de pago nulos) para probar la robustez del ETL.

### 2. Ingesta Optimizada (`load_data.py`)
En lugar de usar el estándar `pd.to_sql` (que es lento para estos volúmenes), implementé el comando **`COPY` de PostgreSQL** a través de `psycopg2`.
- **Resultado:** Reducción del tiempo de carga de ~40s a **<1 segundo**.

### 3. Transformación SQL (`transform_sales.py`)
La lógica de negocio se ejecuta directamente en el motor de base de datos (Postgres) para aprovechar su eficiencia.
- Limpieza de datos nulos.
- Cálculo de columnas derivadas (`total_venta`).
- **Lógica de Fraude:** Flagging automático de transacciones > $4,000 o devoluciones (valores negativos).

### 4. Infraestructura
Todo corre sobre contenedores **Docker** definidos en `docker-compose.yml`, garantizando que el entorno (versión de Python, versión de Postgres) sea reproducible en cualquier máquina.

## Cómo ejecutarlo

1. Levantar la base de datos:
   ```bash
   docker compose up -d
   ```

2. Correr el pipeline completo:
   ```bash
   python main_pipeline.py
   ```
   *Esto ejecutará secuencialmente la generación, carga y transformación.*

## Resultados
En mi entorno local (WSL2), el pipeline completo procesa 500,000 registros en aproximadamente **4.8 segundos**.

---
*Repo creado como parte de mi ruta de aprendizaje de Ingeniería de Datos.*
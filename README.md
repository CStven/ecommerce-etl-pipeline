# Real-time E-Commerce ETL Pipeline

**Proyecto de detección de fallas y análisis financiero.**

Este proyecto simula un entorno de alto volumen transaccional (500k registros/día) para procesar ventas, detectar anomalías y generar reportes financieros automatizados.

## Arquitectura Técnica
*   **Extract:** Generador de datos en Python (Simulación de fallos de API, latencia y datos sucios).
*   **Load:** Ingesta masiva a PostgreSQL usando protocolo `COPY` (<1s para 500k filas).
*   **Transform:** SQL avanzado para limpieza, normalización y reglas de negocio (Flagging de fraudes).
*   **Orquestration:** Pipeline en Python con logging y manejo de errores.
*   **Infra:** Docker & Docker Compose.

## Resultados de Negocio
El pipeline procesó exitosamente 500,000 transacciones con los siguientes KPIs:
*   **Ingresos Validados:** $402M
*   **Fraudes Detectados:** $123M (Transacciones > $4,000 bloqueadas)
*   **Pérdidas por Devolución:** $5.4M
*   **Tiempo Total de Ejecución:** 4.8 segundos (End-to-End)

## Cómo ejecutarlo localmente

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/CStven/ecommerce-etl-pipeline.git
   cd ecommerce-etl-pipeline
   ```

2. **Levantar infraestructura:**
   ```bash
   docker compose up -d
   ```

3. **Ejecutar el Pipeline:**
   ```bash
   python main_pipeline.py
   ```

## Estructura del Proyecto
```text
├── python/
│   ├── generador.py       # Fábrica de datos sintéticos
│   ├── load_data.py       # Cargador optimizado (Postgres COPY)
│   └── transform_sales.py # Lógica de negocio SQL
├── docker-compose.yml     # Configuración de BD
├── main_pipeline.py       # Orquestador
└── README.md
```
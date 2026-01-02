import time
import subprocess
import logging

# Configuración del logging
logging.basicConfig(
    filename='log/main_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def correr_script(script_name):
    """
    Función para correr un script y medir su tiempo de ejecución.
    """
    print(f"Ejecutando {script_name}...")
    logging.info(f"Iniciando {script_name}")
    
    start_time = time.time()
    
    resultado = subprocess.run(["python3", script_name], capture_output=True, text=True)
    
    end_time = time.time() - start_time
    
    if resultado.returncode == 0:
        print(f"{script_name} completado en {end_time:.2f}s")
        logging.info(f"Exito en {script_name} ({end_time:.2f}s)")
        return True
    else:
        print(f"Error en {script_name}!")
        print(resultado.stderr) # Muestra el error técnico
        logging.error(f"Fallo en {script_name}: {resultado.stderr}")
        return False

def main():
    print("Iniciando Pipeline ETL de Ventas")
    
    pasos = [
        "python/generador.py",
        "python/load_data.py",
        "python/transform_sales.py"
    ]
    
    for paso in pasos:
        exito = correr_script(paso)
        if not exito:
            print("Pipeline detenido por errores.")
            break
            
    print("Pipeline finalizado.")

if __name__ == "__main__":
    main()
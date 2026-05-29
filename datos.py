import pandas as pd
import os
from datetime import datetime

class GestorArchivos:
    @staticmethod
    def leer_csv(archivo):
        try:
            return pd.read_csv(archivo)
        except FileNotFoundError:
            print(f"Error: El archivo '{archivo}' no se encontró. Ejecuta 'generar_datos.py' primero.")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo '{archivo}' está vacío.")
            return None
        except Exception as e:
            print(f"Error inesperado al leer '{archivo}': {e}")
            return None

    @staticmethod
    def guardar_csv(df, archivo):
        try:
            df.to_csv(archivo, index=False)
        except Exception as e:
            print(f"Error al guardar los datos en '{archivo}': {e}")

    @staticmethod
    def registrar_asistencia(id_profesor, asistio):
        try:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            nueva_entrada = {'id_profesor': id_profesor, 'fecha': fecha_hoy, 'asistio': asistio}
            df_nueva = pd.DataFrame([nueva_entrada])
            
            archivo = 'asistencia_profesores.csv'
            # Escribe el encabezado solo si el archivo no existe
            escribir_encabezado = not os.path.exists(archivo)
            
            df_nueva.to_csv(archivo, mode='a', header=escribir_encabezado, index=False)
            print(f"Asistencia registrada con éxito para la fecha {fecha_hoy}.")
        except Exception as e:
            print(f"Ocurrió un error al registrar la asistencia: {e}")
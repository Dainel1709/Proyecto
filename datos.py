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
            
    @staticmethod
    def obtener_asistencia_estudiantes(fecha, archivo_grado):
        """
        Busca la asistencia de un grado en una fecha específica.
        Si no existe, carga los estudiantes del grado con asistencia por defecto ('Asistió').
        """
        archivo_asistencia = 'asistencia_estudiantes.csv'
        df_alumnos = pd.read_csv(archivo_grado, dtype=str)
        
        # Si el archivo general de asistencia existe, filtramos por fecha y grado
        if os.path.exists(archivo_asistencia):
            df_asist = pd.read_csv(archivo_asistencia, dtype=str)
            filtro = (df_asist['Fecha'] == fecha) & (df_asist['Archivo_Grado'] == archivo_grado)
            df_fecha = df_asist[filtro]
            
            if not df_fecha.empty:
                # Combinamos para garantizar que se muestren los datos actuales junto con su estado guardado
                df_merge = pd.merge(df_alumnos[['Cédula Identidad', 'Estudiante']], df_fecha[['Cédula Identidad', 'Estado']], on='Cédula Identidad', how='left')
                df_merge['Estado'] = df_merge['Estado'].fillna('Asistió')
                return df_merge.to_dict(orient='records')

        # Si no hay registros previos, inicializamos todos en 'Asistió'
        registros = []
        for _, row in df_alumnos.iterrows():
            registros.append({
                'Cédula Identidad': row.get('Cédula Identidad', row.get('Cédula Escolar', 'S/C')),
                'Estudiante': row['Estudiante'],
                'Estado': 'Asistió'
            })
        return registros

    @staticmethod
    def guardar_asistencia_estudiantes(fecha, archivo_grado, registros_asistencia):
        """
        Guarda o actualiza la lista de asistencia para una sección y fecha concreta.
        """
        archivo_asistencia = 'asistencia_estudiantes.csv'
        df_nuevos = pd.DataFrame(registros_asistencia)
        df_nuevos['Fecha'] = fecha
        df_nuevos['Archivo_Grado'] = archivo_grado
        
        if os.path.exists(archivo_asistencia):
            df_total = pd.read_csv(archivo_asistencia, dtype=str)
            # Eliminamos registros viejos de esta misma fecha y grado para evitar duplicados
            filtro_antiguo = (df_total['Fecha'] == fecha) & (df_total['Archivo_Grado'] == archivo_grado)
            df_total = df_total[~filtro_antiguo]
            # Concatenamos lo nuevo
            df_final = pd.concat([df_total, df_nuevos], ignore_index=True)
        else:
            df_final = df_nuevos
            
        df_final.to_csv(archivo_asistencia, index=False)
    
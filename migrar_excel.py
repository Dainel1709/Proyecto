import pandas as pd
import os
from datetime import datetime

# =========================================================================
# CONFIGURACIÓN DE COLUMNAS (Índices basados en 0 para Python/Pandas)
# =========================================================================
COL_NUMERO_LISTA = 0
COL_CEDULA_ESCOLAR = 1
COL_CEDULA_IDENTIDAD = 2
COL_APELLIDOS_EST = 3
COL_NOMBRES_EST = 4

# Columnas adicionales (si el Excel las tiene)
COL_LUGAR_NAC = 10
COL_REPR_NOMBRE = 11
COL_REPR_CONTACTO = 12
COL_REPR_CORREO = 13
COL_REPR_PARENTESCO = 14
# =========================================================================

def limpiar_dato(valor):
    """Limpia celdas vacías o con formato extraño."""
    if pd.isna(valor): return ""
    txt = str(valor).replace('.0', '').strip()
    return "" if txt.lower() in ['nan', 'none', 'null', ''] else txt

def obtener_valor(row, idx):
    """Devuelve el valor de la fila si el índice existe, sino retorna vacío."""
    if idx < len(row):
        return limpiar_dato(row[idx])
    return ""

def migrar_por_grados_separados():
    print("=== MIGRACIÓN DE FORMATO OFICIAL A CSV POR GRADOS ===")
    
    archivos_esperados = {
        1: 'Matricula_1er_grado.xlsx', 2: 'Matricula_2do_grado.xlsx', 3: 'Matricula_3er_grado.xlsx',
        4: 'Matricula_4to_grado.xlsx', 5: 'Matricula_5to_grado.xlsx', 6: 'Matricula_6to_grado.xlsx'
    }
    
    csv_salida = {
        1: '1er_grado.csv', 2: '2do_grado.csv', 3: '3er_grado.csv',
        4: '4to_grado.csv', 5: '5to_grado.csv', 6: '6to_grado.csv'
    }
    
    for grado, nombre_archivo in archivos_esperados.items():
        if os.path.exists(nombre_archivo):
            print(f"\n-> Procesando {nombre_archivo}...")
            try:
                # header=None para procesar fila por fila manualmente
                df = pd.read_excel(nombre_archivo, header=None)
                estudiantes_grado = []
                
                for index, row in df.iterrows():
                    # 1. Obtener Cédulas
                    val_c1 = obtener_valor(row, COL_CEDULA_ESCOLAR)
                    val_c2 = obtener_valor(row, COL_CEDULA_IDENTIDAD)
                    
                    # Si el número de lista (col 0) está vacío, suele ser una fila de relleno o cabecera
                    if not obtener_valor(row, COL_NUMERO_LISTA).isdigit():
                        continue
                    
                    # 2. Datos del Estudiante
                    apellidos = obtener_valor(row, COL_APELLIDOS_EST)
                    nombres = obtener_valor(row, COL_NOMBRES_EST)
                    
                    # 3. Datos adicionales
                    lugar_nac = obtener_valor(row, COL_LUGAR_NAC)
                    repr_nom = obtener_valor(row, COL_REPR_NOMBRE)
                    repr_cont = obtener_valor(row, COL_REPR_CONTACTO)
                    repr_mail = obtener_valor(row, COL_REPR_CORREO)
                    parentesco = obtener_valor(row, COL_REPR_PARENTESCO)
                    
                    estudiantes_grado.append({
                        'Cédula Escolar': val_c1 if val_c1 else "No posee",
                        'Cédula Identidad': val_c2 if val_c2 else "No posee",
                        'Estudiante': f"{nombres} {apellidos}".strip(),
                        'Lugar de Nacimiento': lugar_nac,
                        'Representante': repr_nom,
                        'Contacto': repr_cont,
                        'Correo Electrónico': repr_mail,
                        'Parentesco': parentesco
                    })
                
                if estudiantes_grado:
                    pd.DataFrame(estudiantes_grado).to_csv(csv_salida[grado], index=False)
                    print(f"   [OK] '{csv_salida[grado]}' guardado con {len(estudiantes_grado)} alumnos.")
                    
            except Exception as e:
                print(f"   [ERROR] No se pudo procesar {nombre_archivo}: {e}")
        else:
            print(f"-> Archivo '{nombre_archivo}' no encontrado.")

if __name__ == "__main__":
    migrar_por_grados_separados()
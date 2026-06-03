import pandas as pd
import os
from openpyxl import load_workbook
from datetime import datetime
# =========================================================================
# CONFIGURACIÓN DE COLUMNAS (Índices basados en 0 para Python/Pandas)
# =========================================================================
COL_NUMERO_LISTA = 0
COL_CEDULA_ESCOLAR = 1
COL_CEDULA_IDENTIDAD = 2
COL_APELLIDOS_EST = 3
COL_NOMBRES_EST = 4
COL_LUGAR_NAC = 5
COL_DIA_NACIMIENTO = 7
COL_MES_NACIMIENTO = 8
COL_ANIO_NACIMIENTO = 9
COL_GERNERO = 10

COL_REPR_APELLIDO = 16
COL_REPR_NOMBRE = 17
COL_REPR_CEDULA_IDENTIDAD = 18
COL_REPR_CONTACTO = 19
COL_REPR_DIRECCION = 20
COL_REPR_PARENTESCO = 21

ARCHIVOS_ESPERADOS = {
    1: 'Matricula_1er_grado.xlsx', 2: 'Matricula_2do_grado.xlsx', 3: 'Matricula_3er_grado.xlsx',
    4: 'Matricula_4to_grado.xlsx', 5: 'Matricula_5to_grado.xlsx', 6: 'Matricula_6to_grado.xlsx'
}

CSV_SALIDA = {
    1: '1er_grado.csv', 2: '2do_grado.csv', 3: '3er_grado.csv',
    4: '4to_grado.csv', 5: '5to_grado.csv', 6: '6to_grado.csv'
}

def limpiar_dato(valor):
    if pd.isna(valor): return ""
    txt = str(valor).replace('.0', '').strip()
    return "" if txt.lower() in ['nan', 'none', 'null', ''] else txt

def obtener_valor(row, idx):
    if idx < len(row):
        return limpiar_dato(row[idx])
    return ""

def convertir_nombre_grado_a_numero(grado_texto):
    """Convierte '1er Grado' o '1er_grado' a un entero (1)"""
    txt = grado_texto.lower()
    for num, nombre in CSV_SALIDA.items():
        if str(num) in txt or nombre.split('_')[0] in txt:
            return num
    return None
def calcular_edad(dia_nac, mes_nac, anio_nac):
    """Calcula la edad exacta basada en la fecha actual del sistema"""
    try:
        # Convertir a enteros por seguridad
        dia = int(float(dia_nac))
        mes = int(float(mes_nac))
        anio = int(float(anio_nac))
        
        hoy = datetime.now()
        # Resta básica de años
        edad = hoy.year - anio
        
        # Verificar si ya pasó su cumpleaños este año (si no, restamos 1)
        if (hoy.month, hoy.day) < (mes, dia):
            edad -= 1
            
        return f"{edad} años"
    except (ValueError, TypeError):
        return "No calculable"
    
# --- FUNCIÓN 1: MIGRACIÓN INICIAL (TU REPO) ---
def migrar_por_grados_separados():
    print("=== MIGRACIÓN DE FORMATO OFICIAL A CSV POR GRADOS ===")
    conteo_creados = 0
    for grado, nombre_archivo in ARCHIVOS_ESPERADOS.items():
        if os.path.exists(nombre_archivo):
            try:
                df = pd.read_excel(nombre_archivo, header=None)
                estudiantes_grado = []
                
                for index, row in df.iterrows():
                    numero_de_lista = obtener_valor(row, COL_NUMERO_LISTA)
                    if not numero_de_lista or not str(numero_de_lista).replace('.0', '').isdigit():
                        continue
                    
                    val_c1 = obtener_valor(row, COL_CEDULA_ESCOLAR)
                    val_c2 = obtener_valor(row, COL_CEDULA_IDENTIDAD)
                    apellidos = obtener_valor(row, COL_APELLIDOS_EST)
                    nombres = obtener_valor(row, COL_NOMBRES_EST)
                    lugar_nac = obtener_valor(row, COL_LUGAR_NAC)
                    dia = obtener_valor(row, COL_DIA_NACIMIENTO)
                    mes = obtener_valor(row, COL_MES_NACIMIENTO)
                    anio = obtener_valor(row, COL_ANIO_NACIMIENTO)
                    genero = obtener_valor(row, COL_GERNERO)
                    
                    repr_apellidos = obtener_valor(row, COL_REPR_APELLIDO)
                    repr_nom = obtener_valor(row, COL_REPR_NOMBRE)
                    repr_cedula = obtener_valor(row, COL_REPR_CEDULA_IDENTIDAD)
                    repr_cont = obtener_valor(row, COL_REPR_CONTACTO)
                    repr_direccion = obtener_valor(row, COL_REPR_DIRECCION)
                    repr_parentesco = obtener_valor(row, COL_REPR_PARENTESCO)
                    
                    estudiantes_grado.append({
                        'Número de lista': int(float(numero_de_lista)),
                        'Cédula Escolar': val_c1 if val_c1 else "No posee",
                        'Cédula Identidad': val_c2 if val_c2 else "No posee",
                        'Estudiante': f"{nombres} {apellidos}".strip(),
                        'Nombres_Est': nombres,
                        'Apellidos_Est': apellidos,
                        'Lugar de Nacimiento': lugar_nac,
                        'Genero': genero,
                        'Fecha de nacimiento': f"{dia}/{mes}/{anio}".strip(),
                        'Dia_Nac': dia, 'Mes_Nac': mes, 'Anio_Nac': anio,
                        'Representante': f"{repr_nom} {repr_apellidos}".strip(),
                        'Repr_Nombre': repr_nom,
                        'Repr_Apellido': repr_apellidos,
                        'Contacto': repr_cont,
                        'Cédula': repr_cedula,
                        'Dirección': repr_direccion,
                        'Parentesco': repr_parentesco
                    })
                
                if estudiantes_grado:
                    pd.DataFrame(estudiantes_grado).to_csv(CSV_SALIDA[grado], index=False, encoding='utf-8-sig')
                    conteo_creados += 1
            except Exception as e:
                print(f"Error procesando {nombre_archivo}: {e}")
    return conteo_creados > 0

# --- FUNCIÓN 2: MODIFICAR DATOS EN EL CSV ---
def modificar_datos_en_csv(grado_texto, cedula_alumno, datos_estudiante=None, datos_representante=None):
    """
    Busca un alumno en el CSV por Cédula o Cédula Escolar y actualiza sus diccionarios de datos.
    """
    num_grado = convertir_nombre_grado_a_numero(grado_texto)
    if not num_grado: return False, "Grado no válido."
    
    nombre_csv = CSV_SALIDA[num_grado]
    if not os.path.exists(nombre_csv):
        return False, f"El archivo CSV {nombre_csv} no existe. Debe cargarlo primero."
        
    df = pd.read_csv(nombre_csv, dtype=str)
    
    # Buscar coincidencia en Cédula Identidad o Cédula Escolar
    idx_busqueda = df[(df['Cédula Identidad'] == str(cedula_alumno)) | (df['Cédula Escolar'] == str(cedula_alumno))].index
    
    if idx_busqueda.empty:
        return False, "Estudiante no encontrado en la base de datos de este grado."
        
    idx = idx_busqueda[0]
    
    # Modificar datos del estudiante por separado si se proveen
    if datos_estudiante:
        if 'Nombres_Est' in datos_estudiante: df.at[idx, 'Nombres_Est'] = datos_estudiante['Nombres_Est']
        if 'Apellidos_Est' in datos_estudiante: df.at[idx, 'Apellidos_Est'] = datos_estudiante['Apellidos_Est']
        if 'Nombres_Est' in datos_estudiante or 'Apellidos_Est' in datos_estudiante:
            df.at[idx, 'Estudiante'] = f"{df.at[idx, 'Nombres_Est']} {df.at[idx, 'Apellidos_Est']}".strip()
        if 'Genero' in datos_estudiante: df.at[idx, 'Genero'] = datos_estudiante['Genero']
        if 'Lugar de Nacimiento' in datos_estudiante: df.at[idx, 'Lugar de Nacimiento'] = datos_estudiante['Lugar de Nacimiento']
        if 'Dia_Nac' in datos_estudiante: df.at[idx, 'Dia_Nac'] = datos_estudiante['Dia_Nac']
        if 'Mes_Nac' in datos_estudiante: df.at[idx, 'Mes_Nac'] = datos_estudiante['Mes_Nac']
        if 'Anio_Nac' in datos_estudiante: df.at[idx, 'Anio_Nac'] = datos_estudiante['Anio_Nac']
        df.at[idx, 'Fecha de nacimiento'] = f"{df.at[idx, 'Dia_Nac']}/{df.at[idx, 'Mes_Nac']}/{df.at[idx, 'Anio_Nac']}"

    # Modificar datos del representante por separado si se proveen
    if datos_representante:
        if 'Repr_Nombre' in datos_representante: df.at[idx, 'Repr_Nombre'] = datos_representante['Repr_Nombre']
        if 'Repr_Apellido' in datos_representante: df.at[idx, 'Repr_Apellido'] = datos_representante['Repr_Apellido']
        if 'Repr_Nombre' in datos_representante or 'Repr_Apellido' in datos_representante:
            df.at[idx, 'Representante'] = f"{df.at[idx, 'Repr_Nombre']} {df.at[idx, 'Repr_Apellido']}".strip()
        if 'Cédula' in datos_representante: df.at[idx, 'Cédula'] = datos_representante['Cédula']
        if 'Contacto' in datos_representante: df.at[idx, 'Contacto'] = datos_representante['Contacto']
        if 'Dirección' in datos_representante: df.at[idx, 'Dirección'] = datos_representante['Dirección']
        if 'Parentesco' in datos_representante: df.at[idx, 'Parentesco'] = datos_representante['Parentesco']

    # Guardar cambios en el CSV
    df.to_csv(nombre_csv, index=False, encoding='utf-8-sig')
    return True, "Datos guardados en CSV exitosamente."

# --- FUNCIÓN 3: SINCRONIZAR CSV HACIA EXCEL ---
def actualizar_excel_desde_csv(grado_texto):
    """ Toma los datos del CSV modificado y reescribe de vuelta el Excel oficial manteniendo su formato básico """
    num_grado = convertir_nombre_grado_a_numero(grado_texto)
    if not num_grado: return False, "Grado no válido."
    
    nombre_excel = ARCHIVOS_ESPERADOS[num_grado]
    nombre_csv = CSV_SALIDA[num_grado]
    
    if not os.path.exists(nombre_csv):
        return False, "No existe el CSV de origen."
    if not os.path.exists(nombre_excel):
        return False, f"El archivo Excel {nombre_excel} no está en la carpeta para actualizar."
        
    try:
        df_csv = pd.read_csv(nombre_csv, dtype=str)
        wb = load_workbook(nombre_excel)
        ws = wb.active # Abre la hoja activa del Excel original
        
        # Iterar por las filas del Excel buscando los números de lista para no desordenar el formato oficial
        for row_idx in range(1, ws.max_row + 1):
            num_lista_excel = limpiar_dato(ws.cell(row=row_idx, column=COL_NUMERO_LISTA + 1).value)
            
            if num_lista_excel.isdigit():
                # Buscar esta fila correspondiente en nuestro dataframe de CSV
                match = df_csv[df_csv['Número de lista'] == num_lista_excel]
                if not match.empty:
                    alumno_datos = match.iloc[0]
                    
                    # Reescribir celdas del Estudiante
                    ws.cell(row=row_idx, column=COL_APELLIDOS_EST + 1, value=alumno_datos.get('Apellidos_Est', ''))
                    ws.cell(row=row_idx, column=COL_NOMBRES_EST + 1, value=alumno_datos.get('Nombres_Est', ''))
                    ws.cell(row=row_idx, column=COL_LUGAR_NAC + 1, value=alumno_datos.get('Lugar de Nacimiento', ''))
                    ws.cell(row=row_idx, column=COL_DIA_NACIMIENTO + 1, value=alumno_datos.get('Dia_Nac', ''))
                    ws.cell(row=row_idx, column=COL_MES_NACIMIENTO + 1, value=alumno_datos.get('Mes_Nac', ''))
                    ws.cell(row=row_idx, column=COL_ANIO_NACIMIENTO + 1, value=alumno_datos.get('Anio_Nac', ''))
                    ws.cell(row=row_idx, column=COL_GERNERO + 1, value=alumno_datos.get('Genero', ''))
                    
                    
                    ws.cell(row=row_idx, column=COL_REPR_APELLIDO + 1, value=alumno_datos.get('Repr_Apellido', ''))
                    ws.cell(row=row_idx, column=COL_REPR_NOMBRE + 1, value=alumno_datos.get('Repr_Nombre', ''))
                    ws.cell(row=row_idx, column=COL_REPR_CEDULA_IDENTIDAD + 1, value=alumno_datos.get('Cédula', ''))
                    ws.cell(row=row_idx, column=COL_REPR_CONTACTO + 1, value=alumno_datos.get('Contacto', ''))
                    ws.cell(row=row_idx, column=COL_REPR_DIRECCION + 1, value=alumno_datos.get('Dirección', ''))
                    ws.cell(row=row_idx, column=COL_REPR_PARENTESCO + 1, value=alumno_datos.get('Parentesco', ''))
        
        wb.save(nombre_excel)
        wb.close()
        return True, f"¡Excel '{nombre_excel}' sincronizado y guardado con éxito!"
    except Exception as e:
        return False, f"Error al escribir en Excel: {e}"
# --- FUNCIÓN 4: AGREGAR UN NUEVO ESTUDIANTE ---
def agregar_estudiante_en_csv(grado_texto, datos_estudiante, datos_representante):
    """
    Añade un estudiante al final del CSV de un grado y recalcula los números de lista.
    """
    num_grado = convertir_nombre_grado_a_numero(grado_texto)
    if not num_grado: return False, "Grado no válido."
    
    nombre_csv = CSV_SALIDA[num_grado]
    if not os.path.exists(nombre_csv):
        return False, f"El archivo CSV {nombre_csv} no existe. Debe cargarlo primero."
        
    try:
        df = pd.read_csv(nombre_csv, dtype=str)
        
        # Validar si la cédula ya existe para no duplicar alumnos
        cedula_nueva = datos_estudiante.get('Cédula Identidad', 'No posee')
        if cedula_nueva != 'No posee' and cedula_nueva in df['Cédula Identidad'].values:
            return False, "Error: Ya existe un estudiante registrado con esa Cédula de Identidad."

        # Calcular el siguiente número de lista de forma automática
        nuevo_num_lista = len(df) + 1
        
        # Unir toda la información en una nueva fila compatible con las columnas del CSV
        nueva_fila = {
            'Número de lista': str(nuevo_num_lista),
            'Cédula Escolar': datos_estudiante.get('Cédula Escolar', 'No posee'),
            'Cédula Identidad': cedula_nueva,
            'Estudiante': f"{datos_estudiante.get('Nombres_Est', '')} {datos_estudiante.get('Apellidos_Est', '')}".strip(),
            'Nombres_Est': datos_estudiante.get('Nombres_Est', ''),
            'Apellidos_Est': datos_estudiante.get('Apellidos_Est', ''),
            'Lugar de Nacimiento': datos_estudiante.get('Lugar de Nacimiento', ''),
            'Genero': datos_estudiante.get('Genero', '').upper(),
            'Fecha de nacimiento': f"{datos_estudiante.get('Dia_Nac', '')}/{datos_estudiante.get('Mes_Nac', '')}/{datos_estudiante.get('Anio_Nac', '')}".strip(),
            'Dia_Nac': datos_estudiante.get('Dia_Nac', ''),
            'Mes_Nac': datos_estudiante.get('Mes_Nac', ''),
            'Anio_Nac': datos_estudiante.get('Anio_Nac', ''),
            'Representante': f"{datos_representante.get('Repr_Nombre', '')} {datos_representante.get('Repr_Apellido', '')}".strip(),
            'Repr_Nombre': datos_representante.get('Repr_Nombre', ''),
            'Repr_Apellido': datos_representante.get('Repr_Apellido', ''),
            'Contacto': datos_representante.get('Contacto', ''),
            'Cédula': datos_representante.get('Cédula', ''),
            'Dirección': datos_representante.get('Dirección', ''),
            'Parentesco': datos_representante.get('Parentesco', '')
        }
        
        # Insertar fila y guardar CSV
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_csv(nombre_csv, index=False, encoding='utf-8-sig')
        return True, "Estudiante agregado al CSV correctamente."
    except Exception as e:
        return False, f"Error al agregar estudiante: {e}"


# --- FUNCIÓN 5: ELIMINAR UN ESTUDIANTE Y REORDENAR ---
def eliminar_estudiante_en_csv(grado_texto, cedula_alumno):
    """
    Elimina un estudiante por su cédula (Identidad o Escolar) y reordena los números de lista correlativamente.
    """
    num_grado = convertir_nombre_grado_a_numero(grado_texto)
    if not num_grado: return False, "Grado no válido."
    
    nombre_csv = CSV_SALIDA[num_grado]
    if not os.path.exists(nombre_csv):
        return False, f"El archivo CSV {nombre_csv} no existe."
        
    try:
        df = pd.read_csv(nombre_csv, dtype=str)
        
        # Buscar la fila por Cédula de Identidad o Escolar
        condicion = (df['Cédula Identidad'] == str(cedula_alumno)) | (df['Cédula Escolar'] == str(cedula_alumno))
        idx_busqueda = df[condicion].index
        
        if idx_busqueda.empty:
            return False, "Estudiante no encontrado en la base de datos."
            
        # Eliminar la fila
        df = df.drop(idx_busqueda[0]).reset_index(drop=True)
        
        # REORDENAR: Volver a numerar la columna 'Número de lista' del 1 en adelante
        df['Número de lista'] = [str(i + 1) for i in range(len(df))]
        
        # Guardar cambios
        df.to_csv(nombre_csv, index=False, encoding='utf-8-sig')
        return True, "Estudiante removido de la base de datos y lista reorganizada."
    except Exception as e:
        return False, f"Error al eliminar: {e}"
if __name__ == "__main__":
    migrar_por_grados_separados()
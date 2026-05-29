import pandas as pd
import os
from datetime import datetime

def consolidar_excels_ministerio():
    print("=== MIGRACIÓN DE FORMATO OFICIAL A CSV ===")
    
    lista_grados = []
    # Nombres de los archivos según el grado escolar
    archivos_esperados = {
        1: 'Matricula_1er_grado.xlsx', 2: 'Matricula_2do_grado.xlsx', 3: 'Matricula_3er_grado.xlsx',
        4: 'Matricula_4to_grado.xlsx', 5: 'Matricula_5to_grado.xlsx', 6: 'Matricula_6to_grado.xlsx'
    }
    
    año_actual = datetime.now().year
    archivos_encontrados = 0
    
    for grado, nombre_archivo in archivos_esperados.items():
        if os.path.exists(nombre_archivo):
            print(f"\n-> Procesando {nombre_archivo} (Grado {grado})...")
            try:
                # Se lee sin encabezados para evitar conflictos con la cabecera del Ministerio
                df = pd.read_excel(nombre_archivo, header=None)
                estudiantes_grado = []
                
                # Iterar por cada fila del Excel
                for index, row in df.iterrows():
                    # Buscar el año de nacimiento (suele ubicarse entre la columna 6 y la 10)
                    año_nac = None
                    for col_idx in range(6, 11):
                        try:
                            val = int(row[col_idx])
                            # Validar que sea un año de nacimiento lógico
                            if 2005 <= val <= año_actual:
                                año_nac = val
                                break
                        except (ValueError, TypeError):
                            pass
                    
                    # Si se encuentra un año lógico, asumimos que la fila contiene a un estudiante
                    if año_nac is not None:
                        # Extraer ID (Col 2: Cédula Identidad | Col 1: Cédula Escolar)
                        cedula_id = str(row[2]).replace('.0', '').strip()
                        cedula_escolar = str(row[1]).replace('.0', '').strip()
                        
                        estudiante_id = cedula_id if cedula_id and cedula_id.lower() != 'nan' else cedula_escolar
                        
                        if not estudiante_id or estudiante_id.lower() == 'nan':
                            continue # Ignorar si no hay ninguna cédula
                            
                        # Extraer nombres (Col 3: Apellidos | Col 4: Nombres)
                        apellidos = str(row[3]).strip()
                        nombres = str(row[4]).strip()
                        
                        # Filtro de seguridad por si lee una cabecera accidentalmente
                        if apellidos.lower() == 'apellidos' or nombres.lower() == 'nombres':
                            continue
                            
                        nombre_completo = f"{nombres} {apellidos}"
                        edad = año_actual - año_nac
                        
                        estudiantes_grado.append({
                            'id': estudiante_id,
                            'nombre': nombre_completo,
                            'grado': grado,
                            'edad': edad
                        })
                
                if estudiantes_grado:
                    lista_grados.append(pd.DataFrame(estudiantes_grado))
                    archivos_encontrados += 1
                    print(f"   [OK] Se extrajeron {len(estudiantes_grado)} estudiantes exitosamente.")
                else:
                    print(f"   [AVISO] No se encontraron datos válidos de estudiantes en {nombre_archivo}.")
                    
            except Exception as e:
                print(f"   [ERROR] Al procesar {nombre_archivo}: {e}")
        else:
            print(f"-> Archivo no encontrado: {nombre_archivo}")
    
    if lista_grados:
        # Unir todos los grados y eliminar posibles alumnos duplicados por ID
        df_total = pd.concat(lista_grados, ignore_index=True)
        df_total = df_total.drop_duplicates(subset=['id'])
        
        # Guardar en la base de datos CSV principal
        df_total.to_csv('estudiantes.csv', index=False)
        print(f"\n[ÉXITO TOTAL] 'estudiantes.csv' creado correctamente con {len(df_total)} estudiantes únicos.")
    else:
        print("\n[ERROR] No se generó el CSV. Revisa que los archivos Excel estén en la misma carpeta.")

if __name__ == "__main__":
    consolidar_excels_ministerio()
from modelos import Directora, Administrativo, Profesora
from rol import requiere_rol
from datos import GestorArchivos
import pandas as pd

# --- FUNCIONES PROTEGIDAS POR DECORADORES ---

@requiere_rol('Directora')
def pasar_de_anio(usuario_actual):
    df = GestorArchivos.leer_csv('estudiantes.csv')
    if df is not None:
        df = df[df['grado'] < 6]
        df.loc[:, 'grado'] += 1
        GestorArchivos.guardar_csv(df, 'estudiantes.csv')
        print("-> Promoción exitosa. Los alumnos de 6to grado han egresado.")

@requiere_rol('Profesora') # Directora también accede por la regla del decorador
def actualizar_edades(usuario_actual):
    df = GestorArchivos.leer_csv('estudiantes.csv')
    if df is not None:
        df.loc[:, 'edad'] += 1
        GestorArchivos.guardar_csv(df, 'estudiantes.csv')
        print("-> Edades de los estudiantes actualizadas (+1 año).")

@requiere_rol('Administrativo')
def registrar_asistencia_docente(usuario_actual):
    try:
        id_prof = int(input("Ingrese el ID del profesor: "))
        asistio = input("¿Asistió? (si/no): ").strip().lower()
        if asistio not in ['si', 'no']:
            raise ValueError("Respuesta inválida. Debe ser 'si' o 'no'.")
        GestorArchivos.registrar_asistencia(id_prof, asistio)
    except ValueError as ve:
        print(f"-> Error de entrada: {ve}")

@requiere_rol('Administrativo')
def revisar_asistencia(usuario_actual):
    fecha = input("Ingrese la fecha a consultar (YYYY-MM-DD): ")
    df = GestorArchivos.leer_csv('asistencia_profesores.csv')
    if df is not None:
        resultado = df[df['fecha'] == fecha]
        if resultado.empty:
            print(f"-> No hay registros de asistencia para la fecha {fecha}.")
        else:
            print(f"\n--- Asistencia del {fecha} ---")
            print(resultado)

# --- SISTEMA DE LOGIN Y MENÚ ---

def iniciar_sesion():
    df_personal = GestorArchivos.leer_csv('personal.csv')
    if df_personal is None: return None

    try:
        id_ingresado = int(input("\nIngrese su ID de empleado: "))
        usuario_data = df_personal[df_personal['id'] == id_ingresado]
        
        if usuario_data.empty:
            print("-> ID no encontrado en el sistema.")
            return None
            
        nombre = usuario_data.iloc[0]['nombre']
        rol = usuario_data.iloc[0]['rol']
        
        # Aplicamos Polimorfismo al crear la instancia
        if rol == 'Directora':
            return Directora(id_ingresado, nombre, rol)
        elif rol == 'Administrativo':
            return Administrativo(id_ingresado, nombre, rol)
        elif rol == 'Profesora':
            return Profesora(id_ingresado, nombre, rol)
            
    except ValueError:
        print("-> Error: El ID debe ser un número entero.")
        return None

def ejecutar_accion(funcion, usuario_actual):
    # Envolvemos las llamadas en un try-except para capturar el PermissionError del decorador
    try:
        funcion(usuario_actual)
    except PermissionError as pe:
        print(f"\n[ALERTA DE SEGURIDAD] {pe}")

def main():
    print("=== SISTEMA DE GESTIÓN ESCOLAR ===")
    usuario_actual = iniciar_sesion()
    
    if not usuario_actual:
        return
        
    print(f"\n{usuario_actual.mostrar_panel()}")

    while True:
        print("\n--- MENÚ DE ACCIONES ---")
        print("1. Pasar de año (Estudiantes)")
        print("2. Actualizar edad de estudiantes")
        print("3. Registrar asistencia de profesor")
        print("4. Revisar asistencia por fecha")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ejecutar_accion(pasar_de_anio, usuario_actual)
        elif opcion == '2':
            ejecutar_accion(actualizar_edades, usuario_actual)
        elif opcion == '3':
            ejecutar_accion(registrar_asistencia_docente, usuario_actual)
        elif opcion == '4':
            ejecutar_accion(revisar_asistencia, usuario_actual)
        elif opcion == '5':
            print("Cerrando el sistema...")
            break
        else:
            print("-> Opción no válida.")

if __name__ == "__main__":
    main()
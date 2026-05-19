from flask import Flask, render_template, request
from datetime import date
import csv

app = Flask(__name__)

# Función para calcular la edad en tiempo real
def calcular_edad(fecha_nacimiento_str):
    try:
        fecha_nac = date.fromisoformat(fecha_nacimiento_str)
        hoy = date.today()
        edad = hoy.year - fecha_nac.year
        # Resta un año si aún no ha llegado el día de su cumpleaños este año
        if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
            edad -= 1
        return edad
    except ValueError:
        return "Error en fecha"

# Ruta principal: muestra el formulario y los resultados de búsqueda
@app.route('/', methods=['GET'])
def index():
    # Capturar los filtros que el usuario escribe en el HTML
    filtro_nombre = request.args.get('nombre', '').lower()
    filtro_grado = request.args.get('grado', '')
    filtro_seccion = request.args.get('seccion', '').upper()
    filtro_sexo = request.args.get('sexo', '')

    estudiantes_filtrados = []

    # Leer el archivo CSV
    with open('estudiantes.csv', mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        for fila in lector:
            # 1. Calcular la edad en tiempo real antes de mostrarla
            fila['edad'] = calcular_edad(fila['fecha_nacimiento'])
            
            # 2. Aplicar la lógica de filtros de búsqueda
            match_nombre = filtro_nombre in fila['nombre'].lower()
            match_grado = not filtro_grado or fila['grado'] == filtro_grado
            match_seccion = not filtro_seccion or fila['seccion'] == filtro_seccion
            match_sexo = not filtro_sexo or fila['sexo'] == filtro_sexo

            # Si el estudiante cumple con todos los filtros, se añade a la lista
            if match_nombre and match_grado and match_seccion and match_sexo:
                estudiantes_filtrados.append(fila)

    # Enviar los resultados al archivo HTML
    return render_template('index.html', estudiantes=estudiantes_filtrados)

if __name__ == '__main__':
    app.run(debug=True)

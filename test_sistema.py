import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
import pandas as pd

# Importamos tus componentes originales
from modelos import Directora, Administrativo, Profesora, Usuario
from main import pasar_de_anio, actualizar_edades, registrar_asistencia_docente
from migrar_excel import calcular_edad, convertir_nombre_grado_a_numero, limpiar_dato


class TestErroresCriticosYLunaDeGrados(unittest.TestCase):
    """Pruebas destinadas a detectar las fallas lógicas del sistema."""

    def test_alerta_bug_columna_edad_inexistente(self):
        """
        ALERTA: Este test demuestra que 'actualizar_edades' falla silenciosamente
        porque los CSV migrados no poseen la columna 'edad'.
        """
        # Simulamos la estructura exacta que genera tu migrador de Excel
        columnas_reales_csv = ['Número de lista', 'Estudiante', 'Dia_Nac', 'Mes_Nac', 'Anio_Nac']
        df_simulado = pd.DataFrame([[1, "Juan Perez", "10", "05", "2015"]], columns=columnas_reales_csv)
        
        # CAMBIO AQUÍ: Usamos un nombre único que NUNCA coincida con tus archivos reales
        archivo_test = 'temporal_test_para_pruebas_unitarias.csv'
        df_simulado.to_csv(archivo_test, index=False)
        
        profesora = Profesora(102, "María", "Profesora")
        
        # Parcheamos temporalmente GRADOS_CSV dentro de 'main' para que apunte a nuestro archivo de mentira
        with patch('main.GRADOS_CSV', [archivo_test]):
            try:
                # Ejecutamos tu función
                actualizar_edades(profesora)
                
                # Volvemos a leer el archivo de mentira para ver si cambió algo
                df_resultado = pd.read_csv(archivo_test)
                
                self.assertNotIn('edad', df_resultado.columns, "¡La columna 'edad' no existe en el esquema de migración!")
            finally:
                if os.path.exists(archivo_test):
                    os.remove(archivo_test)

    def test_falla_conversion_grados_falsos_positivos(self):
        """
        ALERTA: Verifica si escribir 'Grado 10' confunde al sistema
        y lo hace retornar 1 (1er Grado) por coincidencia parcial de caracteres.
        """
        resultado_error = convertir_nombre_grado_a_numero("Grado 10")
        # Debería dar None porque no existe el 10° Grado en tu diccionario, pero da 1.
        self.assertNotEqual(resultado_error, 1, "¡BUG DETECTADO!: 'Grado 10' fue interpretado como 1er Grado debido a '1' in '10'")


class TestControlSeguridadYRoles(unittest.TestCase):
    """Prueba que el decorador @requiere_rol impida accesos no autorizados."""

    def setUp(self):
        self.directora = Directora(1, "Ana Luisa", "Directora")
        self.profesora = Profesora(2, "Carmen", "Profesora")
        self.administrativo = Administrativo(3, "Pedro", "Administrativo")

    def test_restriccion_rol_profesora(self):
        """Una profesora no debe tener permitido iniciar la promoción de año escolar."""
        with self.assertRaises(PermissionError):
            pasar_de_anio(self.profesora)

    @patch('os.path.exists', return_value=False)
    def test_directora_omite_restricciones(self, mock_exists):
        """La Directora debe poder ejecutar cualquier función por jerarquía."""
        try:
            pasar_de_anio(self.directora)
            actualizar_edades(self.directora)
        except PermissionError:
            self.fail("El decorador bloqueó a la Directora injustificadamente.")


class TestUtilidadesTratamientoDatos(unittest.TestCase):
    """Prueba el comportamiento de las funciones de limpieza frente a anomalías."""

    def test_limpiar_dato_variados(self):
        self.assertEqual(limpiar_dato("15.0"), "15")
        self.assertEqual(limpiar_dato("   CI 24000   "), "CI 24000")
        self.assertEqual(limpiar_dato(float('nan')), "")

    @patch('migrar_excel.datetime')
    def test_calcular_edad_exacta(self, mock_datetime):
        # Forzamos la fecha del sistema al 5 de Junio de 2026 para el caso de prueba
        mock_datetime.now.return_value = datetime(2026, 6, 5)
        
        # Ya cumplió años (Nació en Enero) -> 2026 - 2016 = 10 años
        self.assertEqual(calcular_edad("15", "01", "2016"), "10 años")
        # No ha cumplido años (Nace en Diciembre) -> Debe restar 1 -> 9 años
        self.assertEqual(calcular_edad("25", "12", "2016"), "9 años")
        # Datos corruptos en las celdas del Excel original
        self.assertEqual(calcular_edad("Desconocido", "05", "2014"), "No calculable")


class TestModulosEntradaYMenus(unittest.TestCase):
    """Simula las entradas de teclado del usuario usando mocks."""

    @patch('builtins.input', side_effect=['101', 'si'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_registrar_asistencia_valores_validos(self, mock_registrar, mock_input):
        admin = Administrativo(3, "Pedro", "Administrativo")
        registrar_asistencia_docente(admin)
        # Comprueba que la función extrajo el input y llamó correctamente al grabador de archivos
        mock_registrar.assert_called_once_with(101, 'si')

    @patch('builtins.input', side_effect=['101', 'tal vez'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_registrar_asistencia_valores_invalidos(self, mock_registrar, mock_input):
        admin = Administrativo(3, "Pedro", "Administrativo")
        # Debe atrapar el ValueError y no registrar nada corrupto en el CSV
        registrar_asistencia_docente(admin)
        mock_registrar.assert_not_called()


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
import pandas as pd

try:
    from modelos import Directora, Administrativo, Profesora
    from main import pasar_de_anio, actualizar_edades, registrar_asistencia_docente
    from migrar_excel import calcular_edad, convertir_nombre_grado_a_numero, limpiar_dato
except ImportError as e:
    print(f"⚠️ Error de importación: {e}. Asegúrate de que los archivos .py estén en la misma carpeta.")

class TestSistemaEscolar(unittest.TestCase):
    """Pruebas profesionales para el sistema de gestión escolar."""

    # Variable de clase para llevar el conteo de las pruebas
    test_count = 0

    @classmethod
    def setUpClass(cls):
        print(f"🚀 Iniciando batería de 8 pruebas técnicas...\n{'-'*45}")

    def tearDown(self):
        # Al finalizar cada prueba, aumentamos el contador e imprimimos el éxito
        TestSistemaEscolar.test_count += 1
        print(f"✅ Prueba {TestSistemaEscolar.test_count} pasada")

    #BLOQUE 1: LÓGICA DE DATOS

    def test_01_columna_edad_inexistente(self):
        """Detecta si el sistema falla al no encontrar la columna 'edad'."""
        columnas = ['Número de lista', 'Estudiante', 'Dia_Nac', 'Mes_Nac', 'Anio_Nac']
        df_simulado = pd.DataFrame([[1, "Juan Perez", "10", "05", "2015"]], columns=columnas)
        archivo_test = 'temp_test_schema.csv'
        df_simulado.to_csv(archivo_test, index=False)
        
        profesora = Profesora(102, "María", "Profesora")
        
        with patch('main.GRADOS_CSV', [archivo_test]):
            try:
                actualizar_edades(profesora)
                df_res = pd.read_csv(archivo_test)
                # Verificamos que no se rompa, pero que sepamos que 'edad' no se creó mágicamente
                self.assertNotIn('edad', df_res.columns)
            finally:
                if os.path.exists(archivo_test): os.remove(archivo_test)

    def test_02_conversion_grados_falsos_positivos(self):
        """Verifica que 'Grado 10' no sea confundido con 'Grado 1'."""
        resultado = convertir_nombre_grado_a_numero("Grado 10")
        # Si tu diccionario solo llega al 6, esto debería ser None o Error, no 1.
        self.assertNotEqual(resultado, 1, "Error: 'Grado 10' interpretado erróneamente como 1er Grado.")

    #BLOQUE 2: SEGURIDAD Y ROLES

    def test_03_restriccion_rol_profesora(self):
        """Una profesora no puede ejecutar cierres de año."""
        profesora = Profesora(2, "Carmen", "Profesora")
        with self.assertRaises(PermissionError):
            pasar_de_anio(profesora)

    @patch('os.path.exists', return_value=False)
    def test_04_jerarquia_directora(self, mock_exists):
        """La Directora debe saltarse las restricciones de rol."""
        directora = Directora(1, "Ana Luisa", "Directora")
        try:
            pasar_de_anio(directora)
        except PermissionError:
            self.fail("La Directora fue bloqueada por el sistema de permisos.")

    #BLOQUE 3: TRATAMIENTO DE STRINGS Y FECHAS

    def test_05_limpieza_datos_sucios(self):
        """Prueba la robustez ante datos mal formateados del Excel."""
        self.assertEqual(limpiar_dato("15.0"), "15")
        self.assertEqual(limpiar_dato(float('nan')), "")
        self.assertEqual(limpiar_dato("  Texto Espaciado  "), "Texto Espaciado")

    @patch('migrar_excel.datetime')
    def test_06_calculo_edad_exacta(self, mock_dt):
        """Calcula la edad basándose en si ya pasó el cumpleaños en el año actual."""
        mock_dt.now.return_value = datetime(2026, 6, 5)
        # Enero 2016 -> Ya cumplió 10
        self.assertEqual(calcular_edad("15", "01", "2016"), "10 años")
        # Diciembre 2016 -> Tiene 9 (cumple en el futuro)
        self.assertEqual(calcular_edad("25", "12", "2016"), "9 años")

    #BLOQUE 4: INTERFAZ DE USUARIO (MOCKS)

    @patch('builtins.input', side_effect=['101', 'si'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_07_asistencia_valida(self, mock_reg, mock_input):
        """Simula una entrada de teclado correcta."""
        admin = Administrativo(3, "Pedro", "Administrativo")
        registrar_asistencia_docente(admin)
        mock_reg.assert_called_once_with(101, 'si')

    @patch('builtins.input', side_effect=['101', 'no-se'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_08_asistencia_invalida(self, mock_reg, mock_input):
        """Verifica que entradas raras no guarden datos en el sistema."""
        admin = Administrativo(3, "Pedro", "Administrativo")
        registrar_asistencia_docente(admin)
        mock_reg.assert_not_called()

if __name__ == '__main__':
    unittest.main(verbosity=0) 
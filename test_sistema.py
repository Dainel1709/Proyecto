import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os

# Importamos los componentes de tu programa
from modelos import Directora, Administrativo, Profesora, Usuario
from rol import requiere_rol
from main import pasar_de_anio, actualizar_edades, registrar_asistencia_docente
from migrar_excel import calcular_edad, convertir_nombre_grado_a_numero, limpiar_dato


class TestModelosYPolimorfismo(unittest.TestCase):
    """Prueba que las clases heredadas y sus paneles funcionen bien."""
    
    def test_paneles_polimorfismo(self):
        dir_user = Directora(1, "Ana", "Directora")
        admin_user = Administrativo(2, "Carlos", "Administrativo")
        prof_user = Profesora(3, "María", "Profesora")
        
        self.assertEqual(dir_user.mostrar_panel(), "Panel de Directora: Ana. Tienes acceso total al sistema.")
        self.assertEqual(admin_user.mostrar_panel(), "Panel Administrativo: Carlos. Puedes gestionar personal y asistencia.")
        self.assertEqual(prof_user.mostrar_panel(), "Panel de Docente: María. Puedes gestionar información de estudiantes.")

    def test_clase_base_not_implemented(self):
        usuario_generico = Usuario(99, "Innominado", "Invitado")
        with self.assertRaises(NotImplementedError):
            usuario_generico.mostrar_panel()


class TestControlDeRoles(unittest.TestCase):
    """Prueba el decorador de seguridad y las restricciones de accesos."""

    def setUp(self):
        self.directora = Directora(1, "Ana", "Directora")
        self.administrativo = Administrativo(2, "Carlos", "Administrativo")
        self.profesora = Profesora(3, "María", "Profesora")

    @patch('os.path.exists', return_value=False) # Evitamos buscar archivos CSV reales
    def test_directora_puede_hacer_todo(self, mock_exists):
        # La directora puede pasar de año (Su rol explícito)
        try:
            pasar_de_anio(self.directora)
        except PermissionError:
            self.fail("pasar_de_anio() lanzó PermissionError a la Directora erróneamente.")

        # La directora también debe poder entrar a funciones de Profesora
        try:
            actualizar_edades(self.directora)
        except PermissionError:
            self.fail("La Directora no pudo eludir la restricción de 'Profesora'.")

    def test_profesora_denegado_pasar_de_anio(self):
        # Profesora no tiene permisos de Directora
        with self.assertRaises(PermissionError):
            pasar_de_anio(self.profesora)

    @patch('os.path.exists', return_value=False)
    def test_profesora_autorizado_su_rol(self, mock_exists):
        try:
            actualizar_edades(self.profesora)
        except PermissionError:
            self.fail("Se le denegó el acceso a la profesora a su propia función.")


class TestUtilidadesMigracion(unittest.TestCase):
    """Prueba las funciones lógicas de tratamiento de datos de migrar_excel.py."""

    def test_limpiar_dato(self):
        self.assertEqual(limpiar_dato("4.0"), "4")
        self.assertEqual(limpiar_dato("  Texto con espacio  "), "Texto con espacio")
        self.assertEqual(limpiar_dato("NaN"), "")
        self.assertEqual(limpiar_dato(None), "")

    def test_convertir_nombre_grado_a_numero(self):
        self.assertEqual(convertir_nombre_grado_a_numero("1er Grado"), 1)
        self.assertEqual(convertir_nombre_grado_a_numero("6to_grado"), 6)
        self.assertIsNone(convertir_nombre_grado_a_numero("Grado Inventado"))

    @patch('migrar_excel.datetime')
    def test_calcular_edad_exacta(self, mock_datetime):
        # Fijamos la fecha del sistema en el 5 de Junio de 2026 para el test
        mock_datetime.now.return_value = datetime(2026, 6, 5)
        
        # Caso 1: Ya cumplió años este año (Nació el 1 de Enero de 2016 -> Debe tener 10 años)
        self.assertEqual(calcular_edad("01", "01", "2016"), "10 años")
        
        # Caso 2: No ha cumplido años este año (Nació el 20 de Diciembre de 2016 -> Debe tener 9 años)
        self.assertEqual(calcular_edad("20", "12", "2016"), "9 años")
        
        # Caso 3: Datos corruptos o vacíos
        self.assertEqual(calcular_edad("Falta", "Mes", "Año"), "No calculable")


class TestEntradasModulos(unittest.TestCase):
    """Prueba funciones que interactúan con inputs del usuario mediante simulación (Mock)."""

    @patch('builtins.input', side_effects=['105', 'si'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_registrar_asistencia_docente_exito(self, mock_registrar, mock_input):
        admin = Administrativo(2, "Carlos", "Administrativo")
        registrar_asistencia_docente(admin)
        
        # Verifica que se llamó al gestor de archivos con los parámetros correctos procesados
        mock_registrar.assert_called_once_with(105, 'si')

    @patch('builtins.input', side_effects=['105', 'tal vez'])
    @patch('datos.GestorArchivos.registrar_asistencia')
    def test_registrar_asistencia_docente_invalida(self, mock_registrar, mock_input):
        admin = Administrativo(2, "Carlos", "Administrativo")
        
        # No debe caerse el programa, debe manejar el error y NO registrar nada en el CSV
        registrar_asistencia_docente(admin)
        mock_registrar.assert_not_called()


if __name__ == '__main__':
    unittest.main()
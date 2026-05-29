class Usuario:
    def __init__(self, id_usuario, nombre, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol = rol

    def mostrar_panel(self):
        raise NotImplementedError("La subclase debe implementar este método")

class Directora(Usuario):
    def mostrar_panel(self):
        return f"Panel de Directora: {self.nombre}. Tienes acceso total al sistema."

class Administrativo(Usuario):
    def mostrar_panel(self):
        return f"Panel Administrativo: {self.nombre}. Puedes gestionar personal y asistencia."

class Profesora(Usuario):
    def mostrar_panel(self):
        return f"Panel de Docente: {self.nombre}. Puedes gestionar información de estudiantes."
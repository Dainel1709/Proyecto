# Sistema de Gestión Escolar - U.E. Juana Ramírez

Este es un sistema de escritorio moderno desarrollado en Python para automatizar y optimizar la administración de la matrícula escolar y el control de asistencias en la **U.E. Juana Ramírez**. La aplicación cuenta con una interfaz gráfica estilizada (GUI), gestión de bases de datos locales en formato CSV y sincronización automática con libros de cálculo de Microsoft Excel (`.xlsx`).

## 🚀 Características Principales

- **Control de Acceso Seguro (Login):** Validación de usuarios con asignación de roles jerárquicos (Directora, Administrativo, Docente).
- **Panel de Control Interactivo (Dashboard):** Interfaz limpia con menú lateral dinámico y colapsable basado en CustomTkinter.
- **Gestión de Matrícula Automatizada:** Visualización, búsqueda y filtrado de estudiantes por grados (de 1er a 6to grado).
- **Fichas Completas de Alumnos:** Formularios organizados mediante pestañas para añadir, editar, visualizar y eliminar registros completos de estudiantes junto con los datos de sus representantes legales.
- **Módulo de Asistencia Avanzado:** Ventana emergente interactiva que incluye un componente de calendario personalizado (`CTkCalendario`) para registrar de forma rápida asistencias por días específicos de la semana.
- **Sincronización Bidireccional (CSV ⇄ Excel):** Inyección de datos inmediata desde los archivos de edición rápida local (.csv) hacia las plantillas oficiales del colegio en Excel (.xlsx).

## 🛠️ Tecnologías Utilizadas

- **Python 3.x:** Lenguaje base de desarrollo.
- **CustomTkinter:** Biblioteca avanzada de diseño de interfaces con soporte nativo para modos oscuro/claro y esquemas de color profesionales.
- **Pandas:** Manipulación eficiente y lectura/escritura de estructuras de datos en formato CSV.
- **OpenPyXL / Tkinter:** Motores de soporte para el enlace con hojas de cálculo institucionales y ventanas emergentes de diálogo/Treeviews estándar.

## 📁 Estructura del Proyecto

```bash
├── main.py                # Punto de entrada principal para arrancar la aplicación.
├── login_gui.py           # Componentes visuales (Pantalla de login, Dashboard y Ventanas Modales).
├── datos.py               # Capa de abstracción de datos y gestión de archivos generales.
├── migrar_excel.py        # Algoritmos de migración, actualización de planillas Excel e inyección en CSV.
├── modelos.py             # Definición de estructuras de datos internas.
├── rol.py                 # Lógica de permisos según el perfil de usuario.
└── test_sistema.py        # Pruebas automatizadas y de consistencia del entorno.

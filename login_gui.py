import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os

# Configuración del tema visual global
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

# ==========================================
# 1. CONTENEDOR: PANTALLA DE LOGIN
# ==========================================
class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, callback_login_exitoso):
        super().__init__(master, fg_color="transparent")
        self.callback_login_exitoso = callback_login_exitoso

        # Cuadro centrado de Login
        self.card = ctk.CTkFrame(master=self, corner_radius=15, width=380, height=500)
        self.card.pack_propagate(False)
        self.card.pack(expand=True)     

        # Títulos
        self.label_titulo = ctk.CTkLabel(master=self.card, text="¡Bienvenido!", font=("Helvetica", 28, "bold"))
        self.label_titulo.pack(pady=(40, 5), padx=10)

        self.label_subtitulo = ctk.CTkLabel(master=self.card, text="Control de Matrícula Escolar", font=("Helvetica", 14), text_color="gray")
        self.label_subtitulo.pack(pady=(0, 35), padx=10)

        # Campos de texto
        self.input_cedula = ctk.CTkEntry(master=self.card, placeholder_text="Número de Cédula", width=280, height=45, corner_radius=8)
        self.input_cedula.pack(pady=12, padx=10)

        self.input_clave = ctk.CTkEntry(master=self.card, placeholder_text="Contraseña", show="*", width=280, height=45, corner_radius=8)
        self.input_clave.pack(pady=12, padx=10)

        # Botón
        self.boton_ingresar = ctk.CTkButton(master=self.card, text="Iniciar Sesión", command=self.validar_ingreso, width=280, height=45, font=("Helvetica", 15, "bold"), corner_radius=8)
        self.boton_ingresar.pack(pady=(30, 20), padx=10)

        self.label_footer = ctk.CTkLabel(master=self.card, text="Mérida, Venezuela", font=("Helvetica", 11), text_color="gray")
        self.label_footer.pack(side="bottom", pady=20)

    def validar_ingreso(self):
        cedula = self.input_cedula.get().strip()
        clave = self.input_clave.get().strip()

        if not cedula or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor, introduce tu cédula y contraseña.")
            return

        if not os.path.exists('personal.csv'):
            messagebox.showerror("Error del Sistema", "No se encontró el archivo 'personal.csv'.")
            return

        try:
            df_personal = pd.read_csv('personal.csv')
            df_personal['id'] = df_personal['id'].astype(str)
            usuario = df_personal[df_personal['id'] == cedula]

            if not usuario.empty:
                clave_correcta = str(usuario.iloc[0]['contrasena']).strip()
                nombre_usuario = usuario.iloc[0]['nombre']
                rol_usuario = usuario.iloc[0]['rol']

                if clave == clave_correcta:
                    self.callback_login_exitoso(nombre_usuario, rol_usuario)
                else:
                    messagebox.showerror("Error de Acceso", "La contraseña es incorrecta.")
            else:
                messagebox.showerror("Error de Acceso", "Cédula no registrada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la base de datos: {e}")


# ==========================================
# 2. CONTENEDOR: PANTALLA MENÚ PRINCIPAL
# ==========================================
class FrameMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, nombre_usuario, rol_usuario, callback_cerrar_sesion):
        super().__init__(master, fg_color="transparent")
        self.nombre = nombre_usuario
        self.rol = rol_usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion

        # Configurar columnas para pantalla completa
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="U.E. Juana Ramírez", font=("Helvetica", 18, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))

        self.user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.user_frame.grid(row=1, column=0, padx=10, pady=(0, 30))
        
        self.lbl_user_name = ctk.CTkLabel(self.user_frame, text=self.nombre, font=("Helvetica", 13, "bold"))
        self.lbl_user_name.pack()
        self.lbl_user_role = ctk.CTkLabel(self.user_frame, text=f"Rol: {self.rol}", font=("Helvetica", 11), text_color="#1f538d")
        self.lbl_user_role.pack()

        # Botones de navegación lateral
        self.btn_ver_matricula = ctk.CTkButton(self.sidebar_frame, text="Ver Matrícula Escolar", command=self.vista_ver_matricula, height=35)
        self.btn_ver_matricula.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_notas = ctk.CTkButton(self.sidebar_frame, text="Cargar Notas / Asistencia", command=self.vista_notas, height=35)
        self.btn_notas.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        if self.rol in ["Directora", "Administrativo"]:
            self.btn_admin = ctk.CTkButton(self.sidebar_frame, text="Modificar Alumnos (Admin)", fg_color="#2b719e", command=self.vista_administrar, height=35)
            self.btn_admin.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_salir = ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", fg_color="#912a2a", hover_color="#701e1e", command=self.callback_cerrar_sesion, height=35)
        self.btn_salir.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        # --- ÁREA DE CONTENIDO (DERECHA) ---
        self.contenido_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.contenido_frame.grid_columnconfigure(0, weight=1)
        self.contenido_frame.grid_rowconfigure(3, weight=1) # El cuadro de datos (fila 3) se estira al maximizar

        self.lbl_bienvenida = ctk.CTkLabel(self.contenido_frame, text=f"¡Hola, {self.nombre.split()[0]}! Bienvenido al Sistema Académico.", font=("Helvetica", 22, "bold"), anchor="w")
        self.lbl_bienvenida.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.lbl_info_seccion = ctk.CTkLabel(self.contenido_frame, text="Selecciona una opción del menú de la izquierda para comenzar.", font=("Helvetica", 13), text_color="gray", anchor="w")
        self.lbl_info_seccion.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        # --- NUEVO CONTENEDOR DE FILTROS POR GRADO (Línea horizontal) ---
        self.frame_grados = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        # Nota: No lo mostramos con .grid() inmediatamente, solo cuando eligen "Ver Matrícula"
        
        self.lbl_selector = ctk.CTkLabel(self.frame_grados, text="Seleccione el Grado a Consultar:", font=("Helvetica", 13, "bold"))
        self.lbl_selector.pack(side="left", padx=(10, 15))
        
        self.combo_grado = ctk.CTkOptionMenu(
            self.frame_grados, 
            values=["1er Grado", "2do Grado", "3er Grado", "4to Grado", "5to Grado", "6to Grado"],
            command=self.cargar_estudiantes_por_grado,
            width=180
        )
        self.combo_grado.pack(side="left")

        # PANTALLA DE TEXTO PRINCIPAL
        self.pantalla_datos = ctk.CTkTextbox(self.contenido_frame, font=("Courier New", 12), corner_radius=10)
        self.pantalla_datos.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.pantalla_datos.insert("0.0", ">>> Sistema listo.\n>>> Base de datos conectada.")
        self.pantalla_datos.configure(state="disabled")
        self.df_actual = None 

        # Creamos la tabla (Treeview) una sola vez
        columnas = ('Numero de lista','Cédula Escolar','Cédula Identidad', 'Estudiante', 'Genero', 'Fecha de nacimiento')
        self.tabla = ttk.Treeview(self.contenido_frame, columns=columnas, show='headings')
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)
        self.tabla.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Botón Ver Representante
        self.btn_detalle = ctk.CTkButton(self.contenido_frame, text="Ver Representante", command=self.mostrar_detalle_representante)
        self.btn_detalle.grid(row=4, column=0, pady=10)

    # --- CAMBIOS DE VISTA DE CONTENIDO ---
    def vista_ver_matricula(self):
        # Hacemos aparecer sutilmente la barra selectora de grados en la fila 2
        self.frame_grados.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        self.lbl_info_seccion.configure(text="Visualizando las listas oficiales desglosadas por grados.")
        
        # Cargar por defecto el grado que esté seleccionado actualmente en el combo
        self.cargar_estudiantes_por_grado(self.combo_grado.get())

    def vista_notas(self):
        # Ocultamos el filtro de grados porque aquí no se usa
        self.frame_grados.grid_forget()
        
        self.lbl_info_seccion.configure(text="Módulo para el registro de calificaciones y asistencias por lapsos.")
        self.pantalla_datos.configure(state="normal")
        self.pantalla_datos.delete("0.0", "end")
        self.pantalla_datos.insert("0.0", f"=== CARGA DE NOTAS Y EVALUACIÓN ===\n\nDocente: {self.nombre}\nEstatus: Sección en desarrollo institucional...")
        self.pantalla_datos.configure(state="disabled")

    def vista_administrar(self):
        # Ocultamos el filtro de grados
        self.frame_grados.grid_forget()
        
        self.lbl_info_seccion.configure(text="Sección restringida para la modificación, ingresos o retiros de la matrícula.")
        self.pantalla_datos.configure(state="normal")
        self.pantalla_datos.delete("0.0", "end")
        self.pantalla_datos.insert("0.0", f"=== CONFIGURACIÓN DE MATRÍCULA (NIVEL: {self.rol.upper()}) ===\n\nPermisos validados. Aquí se habilitarán los formularios gráficos para añadir o remover estudiantes.")
        self.pantalla_datos.configure(state="disabled")

    # --- LÓGICA DE LECTURA DE ARCHIVOS POR SEPARADO ---
    def cargar_estudiantes_por_grado(self, grado_seleccionado):
        nombre_archivo = f"{grado_seleccionado.lower().replace(' ', '_')}.csv"
    
        # 1. Limpiar tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)
    
        # 2. Cargar datos
        if os.path.exists(nombre_archivo):
            try:
                self.df_actual = pd.read_csv(nombre_archivo)
                # Solo iteramos sobre las filas del DataFrame
                for _, row in self.df_actual.iterrows():
                    self.tabla.insert("", "end", values=(
                        row['Número de lista'], 
                        row['Cédula Escolar'],
                        row['Cédula Identidad'],
                        row['Estudiante'], 
                        row['Genero'], 
                        row['Fecha de nacimiento']
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        else:
            messagebox.showerror("Error", f"Archivo {nombre_archivo} no encontrado.")
    def mostrar_detalle_representante(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            messagebox.showwarning("Selección", "Por favor, seleccione un estudiante de la tabla.")
            return
            
        valores = self.tabla.item(item_seleccionado)['values']
        nombre_est = valores[3]
        
        # Buscar el registro completo en el DataFrame guardado
        datos_est = self.df_actual[self.df_actual['Estudiante'] == nombre_est].iloc[0]
        
        # Crear ventana emergente (Toplevel)
        top = ctk.CTkToplevel(self)
        top.title(f"Representante de {nombre_est}")
        top.geometry("400x300")
        
        info = (f"Representante: {datos_est['Representante']}\n"
                f"Cédula: {datos_est['Cédula']}\n"
                f"Contacto: {datos_est['Contacto']}\n"
                f"Parentesco: {datos_est['Parentesco']}\n"
                f"Dirección: {datos_est['Dirección']}")
                
        ctk.CTkLabel(top, text="Datos del Representante", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(top, text=info, justify="left").pack(pady=10, padx=20)


# ==========================================
# 3. VENTANA MAESTRA ÚNICA
# ==========================================
class AppEscuela(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión - U.E. Juana Ramírez")
        self.geometry("1100x650")
        self.resizable(True, True)

        # Arrancar maximizado directamente
        self.after(50, lambda: self.state('zoomed'))

        self.frame_actual = None
        self.mostrar_pantalla_login()

    def mostrar_pantalla_login(self):
        if self.frame_actual is not None:
            self.frame_actual.destroy()

        self.frame_actual = FrameLogin(self, callback_login_exitoso=self.mostrar_pantalla_dashboard)
        self.frame_actual.pack(fill="both", expand=True)

    def mostrar_pantalla_dashboard(self, nombre, rol):
        if self.frame_actual is not None:
            self.frame_actual.destroy()

        self.frame_actual = FrameMenuPrincipal(self, nombre, rol, callback_cerrar_sesion=self.mostrar_pantalla_login)
        self.frame_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppEscuela()
    app.mainloop()